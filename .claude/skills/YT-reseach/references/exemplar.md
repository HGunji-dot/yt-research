# 模範解答パターン

## 成功する図解の構造

```
1. ヘッダー（グリーングラデーション背景）
   └─ カテゴリバッジ + 作成日 + タイトル + 一言要約

2. インサイトボックス（最重要発見）
   └─ 今すぐ企画に使える気づき1〜2文

3. メインデータセクション（タイプ別）
   └─ トレンド表 / ベンチマークカード / キーワードグリッド など

4. 補足セクション（詳細・深掘り）
   └─ パターン分析・季節性・競合傾向

5. 企画アイデアセクション（必ず最後）
   └─ 3〜5案、各案に根拠・推奨時期あり
```

---

## 企画アイデアセクション（3カテゴリ分類型）の完全パターン

企画アイデアは必ず「作業系」「植物系」「イベント・特集系」の3カテゴリに分けて提案する。

```html
<div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
  <div class="flex items-center gap-3 mb-5">
    <div class="w-10 h-10 bg-green-700 rounded-lg flex items-center justify-center">
      <i data-lucide="lightbulb" class="w-5 h-5 text-yellow-300"></i>
    </div>
    <div>
      <h2 class="text-lg font-bold text-gray-800">企画アイデア</h2>
      <p class="text-xs text-gray-400">【時期】公開向け・3カテゴリ別候補</p>
    </div>
  </div>

  <!-- カテゴリ1: 作業系 -->
  <div class="mb-6">
    <div class="flex items-center gap-2 mb-3">
      <div class="w-6 h-6 bg-orange-100 rounded-md flex items-center justify-center">
        <i data-lucide="scissors" class="w-3.5 h-3.5 text-orange-600"></i>
      </div>
      <span class="text-sm font-bold text-gray-700">作業系</span>
      <span class="text-xs text-gray-400">— この時期の庭仕事・管理テーマ</span>
    </div>
    <div class="space-y-3">

      <!-- 作業系 最優先 -->
      <div class="border-l-4 border-orange-500 bg-orange-50 p-4 rounded-r-xl">
        <div class="flex items-start gap-3">
          <div class="w-7 h-7 bg-orange-500 text-white rounded-full flex items-center justify-center font-bold text-xs flex-shrink-0">★★★</div>
          <div class="flex-1">
            <div class="font-bold text-gray-800 mb-1">【作業系タイトル案】</div>
            <p class="text-sm text-gray-600 mb-2">【内容概要】</p>
            <div class="flex flex-wrap gap-3 text-xs text-gray-500">
              <span class="flex items-center gap-1"><i data-lucide="trending-up" class="w-3 h-3 text-orange-500"></i>根拠：【なぜ今この作業が重要か】</span>
              <span class="flex items-center gap-1"><i data-lucide="calendar" class="w-3 h-3 text-blue-500"></i>推奨：【投稿時期】</span>
            </div>
            <!-- 想定構成（省略可） -->
          </div>
        </div>
      </div>

      <!-- 作業系 2案目以降（同様の構造で繰り返す） -->
    </div>
  </div>

  <!-- カテゴリ2: 植物系 -->
  <div class="mb-6">
    <div class="flex items-center gap-2 mb-3">
      <div class="w-6 h-6 bg-green-100 rounded-md flex items-center justify-center">
        <i data-lucide="leaf" class="w-3.5 h-3.5 text-green-600"></i>
      </div>
      <span class="text-sm font-bold text-gray-700">お庭におすすめの植物</span>
      <span class="text-xs text-gray-400">— 高木・低木・下草・宿根草など</span>
    </div>
    <div class="space-y-3">

      <!-- 植物系カード（種別バッジつき） -->
      <div class="border-l-4 border-green-500 bg-green-50 p-4 rounded-r-xl">
        <div class="flex items-start gap-3">
          <div class="w-7 h-7 bg-green-500 text-white rounded-full flex items-center justify-center font-bold text-xs flex-shrink-0">★★★</div>
          <div class="flex-1">
            <div class="flex items-center gap-2 mb-1 flex-wrap">
              <div class="font-bold text-gray-800">【植物系タイトル案】</div>
              <!-- 種別バッジ（以下から選ぶ） -->
              <span class="bg-green-100 text-green-700 text-xs px-2 py-0.5 rounded-full font-medium">下草・一年草</span>
              <!-- <span class="bg-emerald-100 text-emerald-700 text-xs px-2 py-0.5 rounded-full font-medium">宿根草</span> -->
              <!-- <span class="bg-teal-100 text-teal-700 text-xs px-2 py-0.5 rounded-full font-medium">低木</span> -->
              <!-- <span class="bg-cyan-100 text-cyan-700 text-xs px-2 py-0.5 rounded-full font-medium">高木</span> -->
              <!-- <span class="bg-lime-100 text-lime-700 text-xs px-2 py-0.5 rounded-full font-medium">ハーブ</span> -->
            </div>
            <p class="text-sm text-gray-600 mb-2">【紹介する植物・植え付け・管理のポイント・なぜ今か】</p>
            <div class="flex flex-wrap gap-3 text-xs text-gray-500">
              <span class="flex items-center gap-1"><i data-lucide="trending-up" class="w-3 h-3 text-green-600"></i>根拠：【季節性・需要の根拠】</span>
              <span class="flex items-center gap-1"><i data-lucide="calendar" class="w-3 h-3 text-blue-500"></i>推奨：【投稿時期】</span>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>

  <!-- カテゴリ3: イベント・特集系 -->
  <div class="mb-5">
    <div class="flex items-center gap-2 mb-3">
      <div class="w-6 h-6 bg-purple-100 rounded-md flex items-center justify-center">
        <i data-lucide="star" class="w-3.5 h-3.5 text-purple-600"></i>
      </div>
      <span class="text-sm font-bold text-gray-700">イベント・特集系</span>
      <span class="text-xs text-gray-400">— 品種紹介・特集動画・ランキングなど</span>
    </div>
    <div class="space-y-3">

      <div class="border-l-4 border-purple-400 bg-purple-50 p-4 rounded-r-xl">
        <div class="flex items-start gap-3">
          <div class="w-7 h-7 bg-purple-400 text-white rounded-full flex items-center justify-center font-bold text-xs flex-shrink-0">★★☆</div>
          <div class="flex-1">
            <div class="font-bold text-gray-800 mb-1">【イベント系タイトル案】</div>
            <p class="text-sm text-gray-600 mb-2">【内容概要：品種紹介・特集・ランキングなど】</p>
            <div class="flex flex-wrap gap-3 text-xs text-gray-500">
              <span class="flex items-center gap-1"><i data-lucide="star" class="w-3 h-3 text-purple-500"></i>根拠：【なぜこのタイミングでこの特集か】</span>
              <span class="flex items-center gap-1"><i data-lucide="calendar" class="w-3 h-3 text-blue-500"></i>推奨：【投稿時期】</span>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>

  <!-- 台本キーワードメモ -->
  <div class="bg-gray-50 rounded-lg p-4">
    <div class="flex items-center gap-2 text-xs font-bold text-gray-600 mb-2">
      <i data-lucide="pen-line" class="w-3 h-3"></i>台本・タイトルに入れると良いキーワード
    </div>
    <div class="flex flex-wrap gap-2">
      <span class="bg-white border border-gray-200 text-gray-600 text-xs px-2 py-1 rounded">【キーワード1】</span>
      <span class="bg-white border border-gray-200 text-gray-600 text-xs px-2 py-1 rounded">【キーワード2】</span>
    </div>
  </div>
</div>
```

---

## 企画アイデアセクション（旧・フラットリスト型）パターン

※ 旧パターン。上記3カテゴリ分類型を優先すること。フラットリスト型は後方互換として残す。

```html
<div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
  <div class="flex items-center gap-3 mb-5">
    <div class="w-10 h-10 bg-green-700 rounded-lg flex items-center justify-center">
      <i data-lucide="lightbulb" class="w-5 h-5 text-yellow-300"></i>
    </div>
    <div>
      <h2 class="text-lg font-bold text-gray-800">企画アイデア</h2>
      <p class="text-xs text-gray-400">この図解から導いた動画テーマ候補</p>
    </div>
  </div>

  <div class="space-y-4">
    <!-- 企画案 1（最優先） -->
    <div class="border-l-4 border-green-600 bg-green-50 p-4 rounded-r-xl">
      <div class="flex items-start gap-3">
        <div class="w-8 h-8 bg-green-600 text-white rounded-full flex items-center justify-center font-bold text-sm flex-shrink-0">1</div>
        <div class="flex-1">
          <div class="font-bold text-gray-800 mb-1">【企画タイトル案】</div>
          <p class="text-sm text-gray-600 mb-2">【何を話す動画か1〜2文。視聴者が得るもの・学べることを含める】</p>
          <div class="flex flex-wrap items-center gap-3 text-xs text-gray-500">
            <span class="flex items-center gap-1">
              <i data-lucide="trending-up" class="w-3 h-3 text-green-600"></i>
              根拠：【なぜ今このテーマが良いか。データや季節性を根拠に】
            </span>
            <span class="flex items-center gap-1">
              <i data-lucide="calendar" class="w-3 h-3 text-blue-500"></i>
              推奨投稿時期：【例: 3月中旬〜下旬】
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- 企画案 2 -->
    <div class="border-l-4 border-amber-500 bg-amber-50 p-4 rounded-r-xl">
      <div class="flex items-start gap-3">
        <div class="w-8 h-8 bg-amber-500 text-white rounded-full flex items-center justify-center font-bold text-sm flex-shrink-0">2</div>
        <div class="flex-1">
          <div class="font-bold text-gray-800 mb-1">【企画タイトル案】</div>
          <p class="text-sm text-gray-600 mb-2">【内容概要】</p>
          <div class="flex flex-wrap items-center gap-3 text-xs text-gray-500">
            <span class="flex items-center gap-1">
              <i data-lucide="target" class="w-3 h-3 text-amber-600"></i>
              根拠：【根拠】
            </span>
            <span class="flex items-center gap-1">
              <i data-lucide="calendar" class="w-3 h-3 text-blue-500"></i>
              推奨投稿時期：【時期】
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- 企画案 3 -->
    <div class="border-l-4 border-blue-500 bg-blue-50 p-4 rounded-r-xl">
      <div class="flex items-start gap-3">
        <div class="w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center font-bold text-sm flex-shrink-0">3</div>
        <div class="flex-1">
          <div class="font-bold text-gray-800 mb-1">【企画タイトル案】</div>
          <p class="text-sm text-gray-600 mb-2">【内容概要】</p>
          <div class="flex flex-wrap items-center gap-3 text-xs text-gray-500">
            <span class="flex items-center gap-1">
              <i data-lucide="search" class="w-3 h-3 text-blue-600"></i>
              根拠：【根拠】
            </span>
            <span class="flex items-center gap-1">
              <i data-lucide="calendar" class="w-3 h-3 text-blue-500"></i>
              推奨投稿時期：【時期】
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- 台本キーワードメモ -->
  <div class="mt-5 bg-gray-50 rounded-lg p-4">
    <div class="flex items-center gap-2 text-xs font-bold text-gray-600 mb-2">
      <i data-lucide="pen-line" class="w-3 h-3"></i>
      台本に入れると良いキーワード
    </div>
    <div class="flex flex-wrap gap-2">
      <span class="bg-white border border-gray-200 text-gray-600 text-xs px-2 py-1 rounded">【キーワード1】</span>
      <span class="bg-white border border-gray-200 text-gray-600 text-xs px-2 py-1 rounded">【キーワード2】</span>
      <span class="bg-white border border-gray-200 text-gray-600 text-xs px-2 py-1 rounded">【キーワード3】</span>
    </div>
  </div>
</div>
```

---

## インサイトボックスのパターン

```html
<div class="bg-gradient-to-r from-green-800 to-green-700 text-white rounded-xl p-5">
  <div class="flex items-start gap-3">
    <i data-lucide="lightbulb" class="w-5 h-5 text-yellow-300 flex-shrink-0 mt-0.5"></i>
    <div>
      <div class="font-bold mb-1 text-sm">今月のポイント</div>
      <p class="text-green-100 text-sm leading-relaxed">
        【企画に直結する最重要の発見を1〜2文で。
        「〜が上昇中のため、〜をテーマにした動画が今月有効」のように具体的に】
      </p>
    </div>
  </div>
</div>
```

---

## トレンドテーブルの完全パターン

```html
<div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
  <div class="flex items-center gap-3 mb-5">
    <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
      <i data-lucide="trending-up" class="w-5 h-5 text-green-700"></i>
    </div>
    <div>
      <h2 class="text-lg font-bold text-gray-800">ガーデニングトレンド一覧</h2>
      <p class="text-xs text-gray-400">直近1〜3ヶ月の動向</p>
    </div>
  </div>

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
          <td class="px-4 py-3 font-medium text-gray-800">多肉植物アレンジ</td>
          <td class="px-4 py-3">
            <span class="inline-flex items-center gap-1 text-green-600 font-bold text-xs">
              <i data-lucide="trending-up" class="w-3 h-3"></i>上昇中
            </span>
          </td>
          <td class="px-4 py-3 text-gray-500 text-xs">3〜5月</td>
          <td class="px-4 py-3 text-gray-600 text-xs">初心者向け入門動画と相性良し</td>
        </tr>
        <tr class="hover:bg-gray-50">
          <td class="px-4 py-3 font-medium text-gray-800">ベランダ菜園</td>
          <td class="px-4 py-3">
            <span class="inline-flex items-center gap-1 text-gray-500 font-bold text-xs">
              <i data-lucide="minus" class="w-3 h-3"></i>安定
            </span>
          </td>
          <td class="px-4 py-3 text-gray-500 text-xs">4〜6月</td>
          <td class="px-4 py-3 text-gray-600 text-xs">競合多いが需要も大。差別化必要</td>
        </tr>
        <tr class="hover:bg-gray-50">
          <td class="px-4 py-3 font-medium text-gray-800">ドライフラワーDIY</td>
          <td class="px-4 py-3">
            <span class="inline-flex items-center gap-1 text-red-500 font-bold text-xs">
              <i data-lucide="trending-down" class="w-3 h-3"></i>下降中
            </span>
          </td>
          <td class="px-4 py-3 text-gray-500 text-xs">10〜12月</td>
          <td class="px-4 py-3 text-gray-600 text-xs">冬に仕込むのが吉</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
```

---

## 品質チェックリスト

作成後、以下を全て確認する：

### コンテンツ
- [ ] 企画アイデアセクションが最後にある（3案以上）
- [ ] 各企画アイデアに「なぜ今か」の根拠がある
- [ ] 各企画アイデアに推奨投稿時期がある
- [ ] 台本に使えるキーワードメモがある
- [ ] インサイトボックスで最重要発見を強調している
- [ ] 図解タイプに応じた必須セクションが揃っている（→ diagram-types.md）

### デザイン
- [ ] Lucide iconのみ使用（絵文字なし）
- [ ] ガーデンカラー（green-800/green-600 系統）が適用されている
- [ ] テーブルやカードを使っており、箇条書きだけで済ませていない
- [ ] スマホでも読める（max-w-4xl / レスポンシブ grid）
- [ ] `<style>` タグ・インラインスタイルを追加していない
