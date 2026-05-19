#!/usr/bin/env python3
"""
YouTube Data API v3 を使用してガーデニング系ショート動画データを収集するスクリプト。

使用例:
  # 直近1ヶ月（今月）のショートを収集
  python scripts/youtube_api_research.py --month 5 --year 2026 --category recent_shorts

  # 過去5年・6月公開のショートを収集
  python scripts/youtube_api_research.py --month 6 --years 2021 2022 2023 2024 2025 2026 --category past_shorts

  # 小規模チャンネル（7万人以下）のショートバズを収集
  python scripts/youtube_api_research.py --month 6 --years 2021 2022 2023 2024 2025 2026 --category small_channel_shorts --max-subs 70000

  # ジャンル外チャンネルのショートバズを収集
  python scripts/youtube_api_research.py --month 6 --years 2021 2022 2023 2024 2025 2026 --category genre_out_shorts
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

try:
    from dotenv import load_dotenv
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("依存パッケージが不足しています。以下を実行してください:")
    print("  pip install -r scripts/requirements.txt")
    sys.exit(1)

# ---------------------------------------------------------------------------
# 設定
# ---------------------------------------------------------------------------

GARDENING_KEYWORDS = ["ガーデニング", "植木", "庭木", "剪定", "庭づくり"]

# ジャンル外用キーワード（造園専門でない農業・ライフスタイル系が植木テーマで出す動画を探す）
GENRE_OUT_KEYWORDS = ["庭木 #Shorts", "植木 #Shorts", "シンボルツリー #Shorts", "庭 植物 #Shorts"]

# 尺の判定閾値（秒）
SHORTS_MAX_DURATION_SEC = 60

# API search.list 1回あたりの最大結果数（上限 50）
MAX_RESULTS_PER_SEARCH = 50

# 1回の実行でキープする最大件数（ランキング上位）
DEFAULT_TOP_N = 10

JST = timezone(timedelta(hours=9))

# ---------------------------------------------------------------------------
# ユーティリティ
# ---------------------------------------------------------------------------

def parse_iso8601_duration(duration: str) -> int:
    """ISO 8601 duration string -> seconds.  例: PT1M30S -> 90"""
    pattern = r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?"
    match = re.match(pattern, duration)
    if not match:
        return 0
    h = int(match.group(1) or 0)
    m = int(match.group(2) or 0)
    s = int(match.group(3) or 0)
    return h * 3600 + m * 60 + s


def month_date_range(year: int, month: int):
    """Return (publishedAfter, publishedBefore) in RFC 3339 for a given year/month."""
    after = f"{year}-{month:02d}-01T00:00:00Z"
    if month == 12:
        before = f"{year + 1}-01-01T00:00:00Z"
    else:
        before = f"{year}-{month + 1:02d}-01T00:00:00Z"
    return after, before


# ---------------------------------------------------------------------------
# API 呼び出し
# ---------------------------------------------------------------------------

def search_shorts_for_period(
    youtube,
    keywords: list[str],
    year: int,
    month: int,
    units_counter: list,
) -> list[dict]:
    """
    指定した年月の期間でキーワードごとに search.list を呼び出し、
    videoId / title / channel / publishedAt のリストを返す。
    units_counter[0] に消費ユニット数を累積する。
    """
    after, before = month_date_range(year, month)
    results = []
    seen_ids = set()

    for keyword in keywords:
        # #Shorts を含まないキーワードには付与する
        q = keyword if "#Shorts" in keyword else f"{keyword} #Shorts"
        try:
            response = youtube.search().list(
                q=q,
                type="video",
                publishedAfter=after,
                publishedBefore=before,
                videoDuration="short",   # API 上は「4分未満」= 粗いフィルタ
                order="viewCount",
                maxResults=MAX_RESULTS_PER_SEARCH,
                part="snippet",
                relevanceLanguage="ja",
                regionCode="JP",
            ).execute()
            units_counter[0] += 100  # search.list = 100 units

            for item in response.get("items", []):
                vid_id = item["id"]["videoId"]
                if vid_id in seen_ids:
                    continue
                seen_ids.add(vid_id)
                results.append({
                    "videoId": vid_id,
                    "title": item["snippet"]["title"],
                    "channelTitle": item["snippet"]["channelTitle"],
                    "channelId": item["snippet"]["channelId"],
                    "publishedAt": item["snippet"]["publishedAt"][:10],
                    "keyword": keyword,
                })
        except HttpError as e:
            print(f"  [WARN] search.list error (keyword='{keyword}', {year}/{month:02d}): {e}", file=sys.stderr)

    return results


def fetch_video_details(youtube, video_ids: list[str], units_counter: list) -> dict:
    """
    videos.list で統計情報・コンテンツ詳細を取得して {videoId: {...}} の辞書を返す。
    1 unit/call（バッチ50件）
    """
    details = {}
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i : i + 50]
        try:
            resp = youtube.videos().list(
                id=",".join(batch),
                part="statistics,contentDetails",
            ).execute()
            units_counter[0] += 1  # videos.list = 1 unit per call

            for item in resp.get("items", []):
                vid_id = item["id"]
                duration_str = item["contentDetails"]["duration"]
                dur_sec = parse_iso8601_duration(duration_str)
                stats = item.get("statistics", {})
                details[vid_id] = {
                    "durationSeconds": dur_sec,
                    "isConfirmedShort": dur_sec <= SHORTS_MAX_DURATION_SEC,
                    "viewCount": int(stats.get("viewCount", 0)),
                    "likeCount": int(stats.get("likeCount", 0)),
                    "commentCount": int(stats.get("commentCount", 0)),
                }
        except HttpError as e:
            print(f"  [WARN] videos.list error: {e}", file=sys.stderr)

    return details


def fetch_channel_subscriber_counts(youtube, channel_ids: list[str], units_counter: list) -> dict:
    """
    channels.list で登録者数を取得して {channelId: subscriberCount} を返す。
    small_channel_shorts カテゴリで使用。
    """
    counts = {}
    for i in range(0, len(channel_ids), 50):
        batch = channel_ids[i : i + 50]
        try:
            resp = youtube.channels().list(
                id=",".join(batch),
                part="statistics",
            ).execute()
            units_counter[0] += 1

            for item in resp.get("items", []):
                ch_id = item["id"]
                counts[ch_id] = int(
                    item.get("statistics", {}).get("subscriberCount", 0)
                )
        except HttpError as e:
            print(f"  [WARN] channels.list error: {e}", file=sys.stderr)

    return counts


# ---------------------------------------------------------------------------
# カテゴリ別収集ロジック
# ---------------------------------------------------------------------------

def collect_shorts(
    youtube,
    category: str,
    month: int,
    years: list[int],
    max_subs: int,
    top_n: int,
) -> tuple[list[dict], int]:
    """
    カテゴリに応じてショートデータを収集し、(shorts_list, api_units_used) を返す。
    """
    units_counter = [0]
    keywords = GENRE_OUT_KEYWORDS if category == "genre_out_shorts" else GARDENING_KEYWORDS

    # --- 検索 ---
    raw_videos = []
    for year in years:
        print(f"  Searching {year}/{month:02d} ...", file=sys.stderr)
        found = search_shorts_for_period(youtube, keywords, year, month, units_counter)
        raw_videos.extend(found)
        print(f"    -> {len(found)} candidates (cumulative API units: {units_counter[0]})", file=sys.stderr)

    if not raw_videos:
        return [], units_counter[0]

    # --- 詳細取得（duration 検証 + 再生数）---
    all_ids = [v["videoId"] for v in raw_videos]
    print(f"  Fetching details for {len(all_ids)} videos ...", file=sys.stderr)
    details = fetch_video_details(youtube, all_ids, units_counter)

    # --- 尺フィルタ（真のShortsのみ残す） ---
    confirmed = []
    excluded_count = 0
    for v in raw_videos:
        d = details.get(v["videoId"])
        if d is None:
            excluded_count += 1
            continue
        if not d["isConfirmedShort"]:
            excluded_count += 1
            continue
        confirmed.append({**v, **d})

    # --- small_channel_shorts: 登録者数フィルタ ---
    if category == "small_channel_shorts" and confirmed:
        channel_ids = list({v["channelId"] for v in confirmed})
        print(f"  Fetching subscriber counts for {len(channel_ids)} channels ...", file=sys.stderr)
        sub_counts = fetch_channel_subscriber_counts(youtube, channel_ids, units_counter)
        confirmed_filtered = []
        for v in confirmed:
            subs = sub_counts.get(v["channelId"], 0)
            if subs <= max_subs:
                v["subscriberCount"] = subs
                confirmed_filtered.append(v)
            else:
                excluded_count += 1
        confirmed = confirmed_filtered

    # --- viewCount 降順ソートして上位 N 件 ---
    confirmed.sort(key=lambda x: x.get("viewCount", 0), reverse=True)
    top = confirmed[:top_n]

    # rank 付与 & URL 付与
    for i, v in enumerate(top, 1):
        v["rank"] = i
        v["url"] = f"https://www.youtube.com/shorts/{v['videoId']}"

    print(f"  Confirmed shorts: {len(confirmed)}, excluded: {excluded_count}", file=sys.stderr)
    print(f"  Total API units used: {units_counter[0]}", file=sys.stderr)

    return top, units_counter[0]


# ---------------------------------------------------------------------------
# エントリポイント
# ---------------------------------------------------------------------------

def main():
    # .env 読み込み（スクリプトの親ディレクトリ = YT-reseach ルートを想定）
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent
    env_path = root_dir / ".env"
    load_dotenv(dotenv_path=env_path)

    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        print("Error: YOUTUBE_API_KEY が設定されていません。", file=sys.stderr)
        print(f"  {root_dir / '.env'} を作成し、YOUTUBE_API_KEY=<your_key> を記入してください。", file=sys.stderr)
        sys.exit(1)

    # --- CLI 引数 ---
    parser = argparse.ArgumentParser(
        description="YouTube Data API v3 でガーデニング系ショート動画を収集する"
    )
    parser.add_argument("--month", type=int, required=True, help="収集対象の月 (1-12)")
    parser.add_argument("--year", type=int, help="単一年指定（recent_shorts 用）")
    parser.add_argument("--years", type=int, nargs="+", help="複数年指定（例: 2021 2022 2023）")
    parser.add_argument(
        "--category",
        required=True,
        choices=["recent_shorts", "past_shorts", "small_channel_shorts", "genre_out_shorts"],
        help=(
            "収集カテゴリ: "
            "recent_shorts=直近1ヶ月, "
            "past_shorts=過去5年・同月, "
            "small_channel_shorts=小規模バズ（--max-subs と組み合わせ）, "
            "genre_out_shorts=ジャンル外バズ"
        ),
    )
    parser.add_argument("--max-subs", type=int, default=70000, help="small_channel_shorts: 登録者上限 (default: 70000)")
    parser.add_argument("--top-n", type=int, default=DEFAULT_TOP_N, help="取得件数上限 (default: 10)")
    parser.add_argument("--output", type=str, help="JSON出力先パス（省略時は stdout）")
    args = parser.parse_args()

    # years の解決
    if args.year and not args.years:
        years = [args.year]
    elif args.years:
        years = args.years
    else:
        years = [datetime.now().year]

    print(f"[youtube_api_research] category={args.category}, month={args.month}, years={years}", file=sys.stderr)

    # --- API クライアント構築 ---
    youtube = build("youtube", "v3", developerKey=api_key)

    # --- 収集実行 ---
    shorts, units_used = collect_shorts(
        youtube,
        category=args.category,
        month=args.month,
        years=years,
        max_subs=args.max_subs,
        top_n=args.top_n,
    )

    # --- 出力 ---
    output = {
        "metadata": {
            "collected_at": datetime.now(JST).isoformat(),
            "month": args.month,
            "years": years,
            "category": args.category,
            "total_found": len(shorts),
            "api_units_used": units_used,
        },
        "shorts": shorts,
    }

    json_str = json.dumps(output, ensure_ascii=False, indent=2)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json_str, encoding="utf-8")
        print(f"[youtube_api_research] Saved to {out_path}", file=sys.stderr)
    else:
        print(json_str)


if __name__ == "__main__":
    main()
