/**
 * Google Trends データを取得して trends_data.json に保存するスクリプト
 *
 * 取得内容：
 * 1. 過去5年の月次トレンド（ガーデニング関連キーワード）
 * 2. 5月・6月に絞った月別スコア（季節ピーク確認）
 */

const googleTrends = require("google-trends-api");
const fs = require("fs");

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// 調査するキーワード（バラ・野菜・一年草を除外）
const KEYWORDS = [
  "植木 剪定",
  "庭木 おすすめ",
  "アジサイ 剪定",
  "シンボルツリー",
  "雑草 対策",
];

// 単体キーワード（比較グラフ用。5つ以上は使えない）
const COMPARE_KEYWORDS = [
  "植木 剪定",
  "庭木 おすすめ",
  "アジサイ 剪定",
  "シンボルツリー",
  "雑草 対策",
];

async function fetchInterestOverTime(keywords) {
  try {
    const result = await googleTrends.interestOverTime({
      keyword: keywords,
      startTime: new Date("2021-01-01"),
      endTime: new Date("2026-04-30"),
      geo: "JP",
      hl: "ja",
      granularTimeResolution: false, // 月次で取得
    });
    return JSON.parse(result);
  } catch (e) {
    console.error("  [error]", e.message);
    return null;
  }
}

async function fetchRelatedQueries(keyword) {
  try {
    const result = await googleTrends.relatedQueries({
      keyword,
      startTime: new Date("2024-01-01"),
      endTime: new Date("2026-04-30"),
      geo: "JP",
      hl: "ja",
    });
    const data = JSON.parse(result);
    const top = data?.default?.rankedList?.[0]?.rankedKeyword || [];
    const rising = data?.default?.rankedList?.[1]?.rankedKeyword || [];
    return { top: top.slice(0, 5), rising: rising.slice(0, 5) };
  } catch (e) {
    console.error("  [relatedQueries error]", e.message);
    return { top: [], rising: [] };
  }
}

function extractMonthlyData(trendsData) {
  const timeline = trendsData?.default?.timelineData || [];
  return timeline.map((point) => {
    const date = new Date(parseInt(point.time) * 1000);
    const entry = {
      year: date.getFullYear(),
      month: date.getMonth() + 1, // 1-indexed
      date: `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}`,
    };
    point.value.forEach((v, i) => {
      entry[`kw${i}`] = v;
    });
    return entry;
  });
}

function extractSeasonalAvg(monthly, kwIndex) {
  // 月ごと（1〜12）の平均スコアを計算
  const byMonth = {};
  for (let m = 1; m <= 12; m++) byMonth[m] = [];
  monthly.forEach((d) => {
    if (byMonth[d.month] !== undefined) {
      byMonth[d.month].push(d[`kw${kwIndex}`] || 0);
    }
  });
  const result = {};
  for (let m = 1; m <= 12; m++) {
    const vals = byMonth[m];
    result[m] = vals.length
      ? Math.round(vals.reduce((a, b) => a + b, 0) / vals.length)
      : 0;
  }
  return result;
}

async function main() {
  console.log("Google Trends データ取得開始...\n");

  // 1. 比較トレンド（5キーワード同時）
  console.log("① 比較トレンド取得中:", COMPARE_KEYWORDS.join(" / "));
  const compareData = await fetchInterestOverTime(COMPARE_KEYWORDS);
  await sleep(2000);

  let monthly = [];
  let seasonal = {};

  if (compareData) {
    monthly = extractMonthlyData(compareData);
    COMPARE_KEYWORDS.forEach((kw, i) => {
      seasonal[kw] = extractSeasonalAvg(monthly, i);
    });
    console.log(`  → ${monthly.length} 件の月次データ取得`);
  }

  // 2. 関連クエリ（上昇中キーワード）
  console.log("\n② 関連クエリ取得中...");
  const relatedMap = {};
  for (const kw of ["植木 剪定", "庭木 おすすめ", "雑草 対策"]) {
    console.log(`  「${kw}」`);
    relatedMap[kw] = await fetchRelatedQueries(kw);
    await sleep(1500);
  }

  // 3. 月別スコア（5月・6月フォーカス）
  const mayJuneScores = {};
  COMPARE_KEYWORDS.forEach((kw, i) => {
    if (!seasonal[kw]) return;
    mayJuneScores[kw] = {
      may: seasonal[kw][5] || 0,
      jun: seasonal[kw][6] || 0,
      peak: Object.entries(seasonal[kw]).sort((a, b) => b[1] - a[1])[0],
    };
  });

  const output = {
    generatedAt: new Date().toISOString().slice(0, 16).replace("T", " ") + " JST",
    keywords: COMPARE_KEYWORDS,
    monthly, // 全月次データ
    seasonal, // 月別平均スコア（キーワードごと）
    mayJuneScores, // 5月・6月スコア比較
    relatedQueries: relatedMap,
  };

  fs.writeFileSync("trends_data.json", JSON.stringify(output, null, 2), "utf-8");

  console.log("\n=== 完了 ===");
  console.log(`月次データ: ${monthly.length} 件`);
  console.log("5月・6月スコア:");
  Object.entries(mayJuneScores).forEach(([kw, v]) => {
    console.log(`  「${kw}」5月=${v.may} 6月=${v.jun} ピーク=${v.peak?.[0]}月(${v.peak?.[1]})`);
  });
  console.log("→ trends_data.json に保存");
}

main().catch(console.error);
