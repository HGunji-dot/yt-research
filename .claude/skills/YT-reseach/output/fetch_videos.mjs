/**
 * YouTube Data API v3 で5月〜6月の伸び動画・バズ動画を取得
 * 出力: video_data.json
 */

import https from "https";
import fs from "fs";

const API_KEY = "AIzaSyCZJNbw3G1j9_kC3__AyPn0MxtYKRxggA4";
const BASE = "https://www.googleapis.com/youtube/v3";

// 検索クエリ (バラ・野菜苗・一年草は含めない)
const QUERIES = [
  "植木 庭木",
  "ガーデニング 庭",
  "シンボルツリー",
  "庭木 剪定",
  "低木 おすすめ 庭",
];

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function get(url) {
  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      let data = "";
      res.on("data", (c) => (data += c));
      res.on("end", () => {
        try { resolve(JSON.parse(data)); }
        catch (e) { reject(e); }
      });
    }).on("error", reject);
  });
}

function enc(obj) {
  return Object.entries(obj)
    .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
    .join("&");
}

async function searchVideos(query, publishedAfter, publishedBefore) {
  const params = enc({
    key: API_KEY,
    part: "snippet",
    q: query,
    type: "video",
    regionCode: "JP",
    relevanceLanguage: "ja",
    maxResults: 10,
    order: "viewCount",
    publishedAfter,
    publishedBefore,
  });
  const data = await get(`${BASE}/search?${params}`);
  if (data.error) {
    console.error("  [search error]", data.error.message);
    return [];
  }
  return (data.items || [])
    .filter((i) => i.id?.videoId)
    .map((i) => i.id.videoId);
}

async function getVideoDetails(ids) {
  if (!ids.length) return [];
  const params = enc({ key: API_KEY, part: "statistics,snippet", id: ids.join(",") });
  const data = await get(`${BASE}/videos?${params}`);
  if (data.error) { console.error("  [videos error]", data.error.message); return []; }
  return data.items || [];
}

async function getChannelDetails(ids) {
  const unique = [...new Set(ids)];
  if (!unique.length) return {};
  const params = enc({ key: API_KEY, part: "statistics,snippet", id: unique.join(",") });
  const data = await get(`${BASE}/channels?${params}`);
  if (data.error) { console.error("  [channels error]", data.error.message); return {}; }
  const result = {};
  for (const item of (data.items || [])) {
    result[item.id] = {
      name: item.snippet.title,
      subscriberCount: parseInt(item.statistics?.subscriberCount || "0"),
    };
  }
  return result;
}

function fmtCount(n) {
  if (n >= 10000) return `${(n / 10000).toFixed(1)}万`;
  if (n > 0) return `${n}`;
  return "非公開";
}

async function collectPeriod(label, publishedAfter, publishedBefore) {
  console.log(`\n[${label}] ${publishedAfter.slice(0, 10)} 〜 ${publishedBefore.slice(0, 10)}`);
  const allIds = [];
  for (const q of QUERIES) {
    const ids = await searchVideos(q, publishedAfter, publishedBefore);
    console.log(`  「${q}」: ${ids.length} 件`);
    allIds.push(...ids);
    await sleep(300);
  }
  // 重複排除
  const uniqueIds = [...new Set(allIds)];
  const videos = await getVideoDetails(uniqueIds);
  const channelIds = videos.map((v) => v.snippet.channelId);
  const channels = await getChannelDetails(channelIds);

  const result = videos.map((v) => {
    const stats = v.statistics || {};
    const snippet = v.snippet || {};
    const cid = snippet.channelId;
    const subs = channels[cid]?.subscriberCount || 0;
    const views = parseInt(stats.viewCount || "0");
    return {
      videoId: v.id,
      title: snippet.title,
      channelName: snippet.channelTitle,
      channelId: cid,
      publishedAt: (snippet.publishedAt || "").slice(0, 10),
      viewCount: views,
      viewCountFmt: fmtCount(views),
      subscriberCount: subs,
      subscriberCountFmt: fmtCount(subs),
      url: `https://www.youtube.com/watch?v=${v.id}`,
    };
  });

  result.sort((a, b) => b.viewCount - a.viewCount);
  return result;
}

async function main() {
  const now = new Date();
  const monthAgo = new Date(now - 35 * 86400 * 1000);

  const fmt = (d) => d.toISOString().replace(".000Z", "Z");

  // ① 直近1ヶ月
  const recent = await collectPeriod(
    "直近1ヶ月",
    fmt(monthAgo),
    fmt(now)
  );

  // ② 過去5年の同時期（5月1日〜6月10日）※実行年から自動計算
  const startYear = now.getFullYear() - 5;
  const endYear = now.getFullYear();
  const seasonalAll = [];
  for (let year = startYear; year <= endYear; year++) {
    const items = await collectPeriod(
      `${year}年5〜6月`,
      `${year}-05-01T00:00:00Z`,
      `${year}-06-10T23:59:59Z`
    );
    items.forEach((i) => (i.year = year));
    seasonalAll.push(...items);
    await sleep(500);
  }

  // 重複除去・再生数順
  const seen = new Set();
  const seasonal = [];
  for (const v of seasonalAll.sort((a, b) => b.viewCount - a.viewCount)) {
    if (!seen.has(v.videoId)) {
      seen.add(v.videoId);
      seasonal.push(v);
    }
  }

  // ③ 小規模チャンネルバズ（7万以下）
  const smallChannel = seasonal.filter(
    (v) => v.subscriberCount > 0 && v.subscriberCount <= 70000
  );

  // ④ ジャンル外バズ（登録者10万超 & 再生数が高い）
  // ※ 植木・造園専門チャンネルやベンチマーク対象は除外
  const GENRE_OUTLIER_EXCLUDE = [
    "UCN64oPXNfhEvPQJUaIHAEnA", // カーメン君ガーデンチャンネル（ガーデニング専門）
  ];
  const genreOutlier = seasonal.filter(
    (v) =>
      v.subscriberCount > 100000 &&
      !GENRE_OUTLIER_EXCLUDE.includes(v.channelId) &&
      v.year >= 2021
  );

  const output = {
    generatedAt: now.toISOString().slice(0, 16).replace("T", " ") + " UTC",
    recent_trending: recent.slice(0, 8),
    seasonal_popular: seasonal.slice(0, 10),
    small_channel_buzz: smallChannel.slice(0, 6),
    genre_outlier_buzz: genreOutlier.slice(0, 6),
  };

  fs.writeFileSync("video_data.json", JSON.stringify(output, null, 2), "utf-8");

  console.log("\n=== 完了 ===");
  console.log(`直近1ヶ月 伸び動画:      ${output.recent_trending.length} 件`);
  console.log(`季節的人気動画(5〜6月):  ${output.seasonal_popular.length} 件`);
  console.log(`小規模チャンネルバズ:    ${output.small_channel_buzz.length} 件`);
  console.log(`ジャンル外バズ:          ${output.genre_outlier_buzz.length} 件`);
  console.log("→ video_data.json に保存");
}

main().catch(console.error);
