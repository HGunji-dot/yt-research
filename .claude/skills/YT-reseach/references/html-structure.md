# HTML構造ガイド

## 基本テンプレート

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>【タイトル】</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/lucide@latest"></script>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">
</head>
<body class="bg-stone-50" style="font-family:'Noto Sans JP',sans-serif;">

  <!-- ヘッダー -->
  <header class="bg-gradient-to-r from-green-800 to-green-600 text-white py-8">
    <div class="max-w-4xl mx-auto px-4">
      <div class="flex items-center gap-2 mb-2">
        <span class="text-xs bg-white/20 px-3 py-1 rounded-full">【カテゴリ例: トレンド分析 / ベンチマーク / キーワード / 企画立案】</span>
        <span class="text-xs text-green-200">【作成日 例: 2026年3月】</span>
      </div>
      <h1 class="text-2xl md:text-3xl font-bold">【タイトル】</h1>
      <p class="mt-1 text-green-100 text-sm">【一言要約：この図解から何が分かるか】</p>
    </div>
  </header>

  <!-- メインコンテンツ -->
  <main class="max-w-4xl mx-auto px-4 py-8 space-y-6">
    <!-- セクションはここに挿入 -->
  </main>

  <script>lucide.createIcons();</script>
</body>
</html>
```

---

## セクションカード（共通ベース）

```html
<div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
  <div class="flex items-center gap-3 mb-5">
    <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
      <i data-lucide="trending-up" class="w-5 h-5 text-green-700"></i>
    </div>
    <div>
      <h2 class="text-lg font-bold text-gray-800">セクションタイトル</h2>
      <p class="text-xs text-gray-400">サブテキスト</p>
    </div>
  </div>
  <!-- コンテンツ -->
</div>
```

---

## トレンド方向インジケーター

```html
<!-- ↑ 上昇中 -->
<span class="inline-flex items-center gap-1 text-green-600 font-bold text-sm">
  <i data-lucide="trending-up" class="w-4 h-4"></i>上昇中
</span>

<!-- → 安定 -->
<span class="inline-flex items-center gap-1 text-gray-500 font-bold text-sm">
  <i data-lucide="minus" class="w-4 h-4"></i>安定
</span>

<!-- ↓ 下降中 -->
<span class="inline-flex items-center gap-1 text-red-500 font-bold text-sm">
  <i data-lucide="trending-down" class="w-4 h-4"></i>下降中
</span>
```

---

## キーワードバッジ

```html
<!-- 注目 -->
<span class="inline-flex items-center gap-1 bg-orange-100 text-orange-700 text-xs px-2 py-1 rounded-full font-medium">
  <i data-lucide="flame" class="w-3 h-3"></i>注目
</span>

<!-- 上昇中 -->
<span class="inline-flex items-center gap-1 bg-green-100 text-green-700 text-xs px-2 py-1 rounded-full font-medium">
  <i data-lucide="trending-up" class="w-3 h-3"></i>上昇中
</span>

<!-- 季節性あり -->
<span class="inline-flex items-center gap-1 bg-blue-100 text-blue-700 text-xs px-2 py-1 rounded-full font-medium">
  <i data-lucide="calendar" class="w-3 h-3"></i>季節性
</span>

<!-- 競合多 -->
<span class="inline-flex items-center gap-1 bg-red-100 text-red-600 text-xs px-2 py-1 rounded-full font-medium">
  <i data-lucide="users" class="w-3 h-3"></i>競合多
</span>

<!-- 競合少（ねらい目） -->
<span class="inline-flex items-center gap-1 bg-emerald-100 text-emerald-700 text-xs px-2 py-1 rounded-full font-medium">
  <i data-lucide="target" class="w-3 h-3"></i>ねらい目
</span>
```

---

## 企画アイデアカード

```html
<!-- カード1つ分 -->
<div class="border-l-4 border-green-600 bg-green-50 p-4 rounded-r-xl">
  <div class="flex items-start gap-3">
    <div class="w-8 h-8 bg-green-600 text-white rounded-full flex items-center justify-center font-bold text-sm flex-shrink-0">1</div>
    <div class="flex-1">
      <div class="font-bold text-gray-800 mb-1">【企画タイトル案】</div>
      <p class="text-sm text-gray-600 mb-2">【内容概要：何を話す動画か1〜2文で】</p>
      <div class="flex flex-wrap items-center gap-3 text-xs text-gray-500">
        <span class="flex items-center gap-1">
          <i data-lucide="trending-up" class="w-3 h-3 text-green-600"></i>
          根拠：【なぜ今このテーマが良いか】
        </span>
        <span class="flex items-center gap-1">
          <i data-lucide="calendar" class="w-3 h-3 text-blue-500"></i>
          推奨時期：【例: 3〜4月】
        </span>
      </div>
    </div>
  </div>
</div>
```

---

## トレンド比較テーブル

```html
<div class="overflow-x-auto">
  <table class="w-full text-sm">
    <thead>
      <tr class="bg-green-50">
        <th class="text-left px-4 py-3 text-green-800 font-bold rounded-tl-lg">トレンド</th>
        <th class="text-left px-4 py-3 text-green-800 font-bold">動向</th>
        <th class="text-left px-4 py-3 text-green-800 font-bold">ピーク時期</th>
        <th class="text-left px-4 py-3 text-green-800 font-bold rounded-tr-lg">企画メモ</th>
      </tr>
    </thead>
    <tbody class="divide-y divide-gray-100">
      <tr class="hover:bg-gray-50">
        <td class="px-4 py-3 font-medium text-gray-800">【トレンド名】</td>
        <td class="px-4 py-3">
          <!-- トレンドインジケーターを挿入 -->
        </td>
        <td class="px-4 py-3 text-gray-500 text-xs">【例: 4〜5月】</td>
        <td class="px-4 py-3 text-gray-600 text-xs">【メモ】</td>
      </tr>
    </tbody>
  </table>
</div>
```

---

## ベンチマークYouTuberカード

```html
<div class="bg-white border border-gray-200 rounded-xl p-5">
  <div class="flex items-center gap-3 mb-4">
    <div class="w-10 h-10 bg-red-50 rounded-full flex items-center justify-center">
      <i data-lucide="youtube" class="w-5 h-5 text-red-500"></i>
    </div>
    <div>
      <div class="font-bold text-gray-800">【チャンネル名】</div>
      <div class="text-xs text-gray-400">登録者数: 【規模】 / 月 【投稿頻度】本程度</div>
    </div>
  </div>

  <!-- 直近の動画トピック -->
  <div class="mb-4">
    <div class="text-xs font-bold text-gray-500 uppercase tracking-wide mb-2">直近の動画テーマ</div>
    <div class="space-y-2">
      <div class="flex items-center justify-between py-2 border-b border-gray-50">
        <span class="text-sm text-gray-700">【動画タイトル/テーマ】</span>
        <span class="text-xs bg-gray-100 text-gray-500 px-2 py-0.5 rounded">【再生数】</span>
      </div>
      <!-- 動画行を繰り返す -->
    </div>
  </div>

  <!-- 傾向サマリー -->
  <div class="bg-amber-50 rounded-lg p-3">
    <div class="flex items-center gap-1 text-xs text-amber-700 font-bold mb-1">
      <i data-lucide="lightbulb" class="w-3 h-3"></i>
      最近の方向性
    </div>
    <p class="text-xs text-gray-600">【傾向の1〜2文サマリー】</p>
  </div>
</div>
```

---

## キーワード季節性グリッド（12ヶ月）

```html
<div class="grid grid-cols-4 md:grid-cols-6 gap-2">
  <!-- 各月を繰り返す。検索量が高い月は色を濃くする -->

  <!-- 検索量 高 -->
  <div class="bg-green-200 rounded-lg p-3 text-center">
    <div class="text-xs font-bold text-green-800 mb-1">3月</div>
    <i data-lucide="trending-up" class="w-4 h-4 text-green-700 mx-auto mb-1"></i>
    <div class="text-xs text-green-700">高</div>
  </div>

  <!-- 検索量 中 -->
  <div class="bg-green-100 rounded-lg p-3 text-center">
    <div class="text-xs font-bold text-green-700 mb-1">4月</div>
    <i data-lucide="minus" class="w-4 h-4 text-green-500 mx-auto mb-1"></i>
    <div class="text-xs text-green-500">中</div>
  </div>

  <!-- 検索量 低 -->
  <div class="bg-gray-100 rounded-lg p-3 text-center">
    <div class="text-xs font-bold text-gray-500 mb-1">1月</div>
    <i data-lucide="trending-down" class="w-4 h-4 text-gray-400 mx-auto mb-1"></i>
    <div class="text-xs text-gray-400">低</div>
  </div>
</div>
```

---

## インサイトボックス（重要な発見を強調）

```html
<div class="bg-gradient-to-r from-green-800 to-green-700 text-white rounded-xl p-5">
  <div class="flex items-start gap-3">
    <i data-lucide="lightbulb" class="w-5 h-5 text-yellow-300 flex-shrink-0 mt-0.5"></i>
    <div>
      <div class="font-bold mb-1">重要な発見</div>
      <p class="text-green-100 text-sm">【今すぐ企画に使える気づきを1〜3文で】</p>
    </div>
  </div>
</div>
```

---

## 過去5年の同時期人気動画セクション

公開時期を指定した企画立案図解（タイプ4）に追加するセクション。
同じ時期に過去どんな動画が伸びたかを示し、企画の裏付けに使う。

```html
<div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
  <div class="flex items-center gap-3 mb-5">
    <div class="w-10 h-10 bg-red-50 rounded-lg flex items-center justify-center">
      <i data-lucide="youtube" class="w-5 h-5 text-red-500"></i>
    </div>
    <div>
      <h2 class="text-lg font-bold text-gray-800">過去5年・同時期（5月）の人気動画パターン</h2>
      <p class="text-xs text-gray-400">※ 再生数は公開情報・推定値。実数値はYouTube Studioで要確認</p>
    </div>
  </div>

  <!-- テーマパターン集計 -->
  <div class="mb-5">
    <div class="text-xs font-bold text-gray-500 uppercase tracking-wide mb-3">毎年5月に繰り返し伸びているテーマ（過去5年の傾向）</div>
    <div class="space-y-2">
      <!-- テーマ行（繰り返す） -->
      <div class="flex items-center gap-3 p-3 bg-green-50 rounded-lg border border-green-100">
        <div class="w-8 h-8 bg-green-600 text-white rounded-full flex items-center justify-center flex-shrink-0">
          <i data-lucide="repeat" class="w-4 h-4"></i>
        </div>
        <div class="flex-1">
          <div class="text-sm font-bold text-gray-800">【テーマ名（例: 花後剪定・ツツジ系）】</div>
          <div class="text-xs text-gray-500 mt-0.5">【代表的なタイトルパターン例】</div>
        </div>
        <div class="text-right flex-shrink-0">
          <div class="text-xs font-bold text-green-700">毎年</div>
          <div class="text-xs text-gray-400">出現頻度</div>
        </div>
      </div>
    </div>
  </div>

  <!-- 個別動画リスト -->
  <div class="mb-5">
    <div class="text-xs font-bold text-gray-500 uppercase tracking-wide mb-3">参照動画（過去5年・5月の高評価動画）</div>
    <div class="overflow-x-auto">
      <table class="w-full text-sm">
        <thead>
          <tr class="bg-gray-50">
            <th class="text-left px-3 py-2 text-gray-600 font-bold text-xs rounded-tl-lg">年</th>
            <th class="text-left px-3 py-2 text-gray-600 font-bold text-xs">動画テーマ / タイトルパターン</th>
            <th class="text-left px-3 py-2 text-gray-600 font-bold text-xs">チャンネル</th>
            <th class="text-left px-3 py-2 text-gray-600 font-bold text-xs rounded-tr-lg">推定規模</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr class="hover:bg-gray-50">
            <td class="px-3 py-2 text-gray-500 text-xs">2024</td>
            <td class="px-3 py-2 font-medium text-gray-800 text-sm">【動画テーマ/タイトルパターン】</td>
            <td class="px-3 py-2 text-gray-500 text-xs">【チャンネル名】</td>
            <td class="px-3 py-2">
              <span class="inline-flex items-center gap-1 bg-orange-100 text-orange-700 text-xs px-2 py-0.5 rounded-full">
                <i data-lucide="flame" class="w-3 h-3"></i>高
              </span>
            </td>
          </tr>
          <!-- 行を繰り返す -->
        </tbody>
      </table>
    </div>
  </div>

  <!-- タイトル共通パターン -->
  <div class="bg-amber-50 rounded-lg p-4 border border-amber-100">
    <div class="flex items-center gap-2 text-xs font-bold text-amber-700 mb-2">
      <i data-lucide="lightbulb" class="w-3 h-3"></i>
      伸びているタイトルの共通パターン
    </div>
    <div class="flex flex-wrap gap-2">
      <span class="bg-white border border-amber-200 text-amber-700 text-xs px-2 py-1 rounded">【パターン例: 「今月中に」】</span>
      <span class="bg-white border border-amber-200 text-amber-700 text-xs px-2 py-1 rounded">【パターン例: 「失敗した場合は」】</span>
      <span class="bg-white border border-amber-200 text-amber-700 text-xs px-2 py-1 rounded">【パターン例: 「初心者でも」】</span>
    </div>
  </div>

  <!-- 情報が取得できない場合のフォールバック -->
  <!-- 
  <div class="bg-gray-50 rounded-lg p-4 text-center">
    <i data-lucide="alert-triangle" class="w-5 h-5 text-gray-400 mx-auto mb-2"></i>
    <p class="text-sm text-gray-500">再生数情報の取得には YouTube Studio または Analytics ツールが必要です。</p>
    <p class="text-xs text-gray-400 mt-1">キーワードプランナー・Google Trends で補完してください。</p>
  </div>
  -->
</div>
```

**使用上の注意:**
- YouTube の再生数は公開APIなしでは正確に取得不可。外部メディアや推定値で代替する。
- 情報が十分でない場合は個別動画リストを省略し「テーマパターン集計」のみにする。
- 必ず「推定値」の注記を入れること（冒頭のサブテキストに記載済み）。

---

## よく使う Lucide アイコン一覧

| 用途 | アイコン名 |
|-----|----------|
| トレンド上昇 | `trending-up` |
| トレンド下降 | `trending-down` |
| 安定・横ばい | `minus` |
| 季節・時期 | `calendar` |
| 検索キーワード | `search` |
| YouTube | `youtube` |
| 視聴者・競合 | `users` |
| 企画・アイデア | `lightbulb` |
| ねらい目 | `target` |
| 注目・人気 | `flame` |
| 植物・自然 | `leaf` |
| はさみ・剪定 | `scissors` |
| チェック完了 | `check-circle` |
| 警告・注意 | `alert-triangle` |
| 矢印（右） | `arrow-right` |
| 矢印（下） | `arrow-down` |
| バラ・花 | `flower` |
| 時計・タイミング | `clock` |
