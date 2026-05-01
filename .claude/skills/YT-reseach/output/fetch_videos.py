"""
YouTube Data API v3 を使って、5月〜6月の伸びている動画・バズ動画を取得するスクリプト。
出力: video_data.json (HTML に埋め込むためのデータ)
"""

import requests
import json
from datetime import datetime, timedelta
import time

API_KEY = "AIzaSyCZJNbw3G1j9_kC3__AyPn0MxtYKRxggA4"
BASE_URL = "https://www.googleapis.com/youtube/v3"

# 検索クエリ（除外: バラ・野菜苗・一年草）
QUERIES = ["植木 庭木", "ガーデニング 庭", "シンボルツリー", "庭木 剪定", "低木 おすすめ"]


def search_videos(query, published_after, published_before, max_results=8):
    """指定期間で動画を検索して video_id リストを返す"""
    params = {
        "key": API_KEY,
        "part": "snippet",
        "q": query,
        "type": "video",
        "regionCode": "JP",
        "relevanceLanguage": "ja",
        "maxResults": max_results,
        "order": "viewCount",
        "publishedAfter": published_after,
        "publishedBefore": published_before,
    }
    r = requests.get(f"{BASE_URL}/search", params=params)
    data = r.json()
    if "error" in data:
        print(f"  [ERROR] search: {data['error']['message']}")
        return []
    items = data.get("items", [])
    return [item["id"]["videoId"] for item in items if item["id"].get("videoId")]


def get_video_details(video_ids):
    """video_ids のリストから統計情報を取得する"""
    if not video_ids:
        return []
    params = {
        "key": API_KEY,
        "part": "statistics,snippet",
        "id": ",".join(video_ids),
    }
    r = requests.get(f"{BASE_URL}/videos", params=params)
    data = r.json()
    if "error" in data:
        print(f"  [ERROR] videos: {data['error']['message']}")
        return []
    return data.get("items", [])


def get_channel_details(channel_ids):
    """channel_ids のリストから登録者数などを取得する"""
    if not channel_ids:
        return {}
    unique_ids = list(set(channel_ids))
    params = {
        "key": API_KEY,
        "part": "statistics,snippet",
        "id": ",".join(unique_ids),
    }
    r = requests.get(f"{BASE_URL}/channels", params=params)
    data = r.json()
    if "error" in data:
        print(f"  [ERROR] channels: {data['error']['message']}")
        return {}
    result = {}
    for item in data.get("items", []):
        cid = item["id"]
        stats = item.get("statistics", {})
        result[cid] = {
            "name": item["snippet"]["title"],
            "subscriberCount": int(stats.get("subscriberCount", 0)),
            "videoCount": int(stats.get("videoCount", 0)),
        }
    return result


def fmt_count(n):
    """数値を「12.3万」形式に整形"""
    if n >= 10000:
        return f"{n/10000:.1f}万"
    return str(n)


def collect_videos(label, published_after, published_before):
    """
    指定期間の動画を QUERIES 全部で検索し、
    動画詳細・チャンネル詳細をまとめて返す。
    重複を除いて上位 N 本に絞る。
    """
    print(f"\n[{label}] {published_after} 〜 {published_before}")
    all_ids = []
    for q in QUERIES:
        ids = search_videos(q, published_after, published_before)
        print(f"  クエリ「{q}」: {len(ids)} 件")
        all_ids.extend(ids)
        time.sleep(0.3)

    # 重複排除
    all_ids = list(dict.fromkeys(all_ids))

    videos = get_video_details(all_ids)

    # チャンネル詳細
    channel_ids = [v["snippet"]["channelId"] for v in videos]
    channels = get_channel_details(channel_ids)

    result = []
    for v in videos:
        stats = v.get("statistics", {})
        snippet = v.get("snippet", {})
        view_count = int(stats.get("viewCount", 0))
        channel_id = snippet.get("channelId", "")
        channel_info = channels.get(channel_id, {})
        subs = channel_info.get("subscriberCount", 0)

        pub_date = snippet.get("publishedAt", "")[:10]

        result.append({
            "videoId": v["id"],
            "title": snippet.get("title", ""),
            "channelName": snippet.get("channelTitle", ""),
            "channelId": channel_id,
            "publishedAt": pub_date,
            "viewCount": view_count,
            "viewCountFmt": fmt_count(view_count),
            "subscriberCount": subs,
            "subscriberCountFmt": fmt_count(subs),
            "url": f"https://www.youtube.com/watch?v={v['id']}",
        })

    # 再生数降順でソート
    result.sort(key=lambda x: x["viewCount"], reverse=True)
    return result


def main():
    now = datetime.utcnow()

    # ① 直近1ヶ月（2026年4〜5月）
    recent_after = (now - timedelta(days=35)).strftime("%Y-%m-%dT00:00:00Z")
    recent_before = now.strftime("%Y-%m-%dT23:59:59Z")
    recent = collect_videos("直近1ヶ月", recent_after, recent_before)

    # ② 過去7年の同時期（5月1日〜6月10日）
    seasonal_all = []
    for year in range(2020, 2027):
        after = f"{year}-05-01T00:00:00Z"
        before = f"{year}-06-10T23:59:59Z"
        items = collect_videos(f"{year}年5〜6月", after, before)
        for item in items:
            item["year"] = year
        seasonal_all.extend(items)
        time.sleep(0.5)

    # 再生数降順でソート・重複除去
    seen = set()
    seasonal_dedup = []
    for v in sorted(seasonal_all, key=lambda x: x["viewCount"], reverse=True):
        if v["videoId"] not in seen:
            seen.add(v["videoId"])
            seasonal_dedup.append(v)

    # ③ 小規模チャンネルのバズ動画（登録者7万以下）
    small_channel = [v for v in seasonal_dedup if 0 < v["subscriberCount"] <= 70000]

    # ④ ジャンル外バズ（登録者10万以上 でも再生数が高い＝ジャンル外から流入している可能性）
    #    実際の「ジャンル外」判定はチャンネルカテゴリが必要だが、
    #    ここでは登録者が多い（10万超）のに植木テーマで伸びているものを暫定で抽出
    genre_outlier = [v for v in seasonal_dedup if v["subscriberCount"] > 100000]

    output = {
        "generatedAt": now.strftime("%Y-%m-%d %H:%M UTC"),
        "recent_trending": recent[:8],
        "seasonal_popular": seasonal_dedup[:10],
        "small_channel_buzz": small_channel[:6],
        "genre_outlier_buzz": genre_outlier[:6],
    }

    out_path = "video_data.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n=== 完了 ===")
    print(f"直近1ヶ月 伸び動画:     {len(output['recent_trending'])} 件")
    print(f"季節的人気動画（5〜6月）: {len(output['seasonal_popular'])} 件")
    print(f"小規模チャンネルバズ:   {len(output['small_channel_buzz'])} 件")
    print(f"ジャンル外バズ:         {len(output['genre_outlier_buzz'])} 件")
    print(f"→ {out_path} に保存しました")


if __name__ == "__main__":
    main()
