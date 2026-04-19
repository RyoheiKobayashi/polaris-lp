# scripts/

glossary 運用用のツール置き場。

## ファイル一覧

| ファイル | 用途 |
|---|---|
| `detail-page-template.html` | 詳細ページの雛形（穴埋めプレースホルダ付き） |
| `audit-examples.py` | 全用語の「身近な例え」を抽出して `examples-audit.md` に出力 |

---

## 詳細ページの追加手順

新しい用語を追加する時の流れ。

### 1. プレースホルダの中身を決める

| プレースホルダ | 意味 | 例 |
|---|---|---|
| `{{NUM}}` | 通し番号（0埋め無し） | `86` |
| `{{CAT}}` | カテゴリ記号 | `H` |
| `{{CAT_LABEL}}` | カテゴリ日本語名 | `セキュリティ` |
| `{{EN}}` | 英名 | `Prompt Injection` |
| `{{NAME}}` | 日本語名（h1に入る） | `プロンプトインジェクション` |
| `{{SUB}}` | 1行サブタイトル | `AIへの「悪意ある命令」の混入` |
| `{{META_DESC}}` | meta description | `AIに悪意の指示を混入させる攻撃を3秒で理解。` |
| `{{HERO_CSS}}` | アニメのCSS（`.hero-xxx { ... }`） | DESIGN.mdの色だけで組む |
| `{{HERO_HTML}}` | アニメのHTML | `<div class="hero-xxx">...</div>` |
| `{{EXPLAIN}}` | 「〇〇ってそもそも何？」の解説 | mark強調つきで1段落 |
| `{{EX1_TITLE}}` / `{{EX1_BODY}}` | 例①のタイトルと本文 | 「家の合鍵」など身近なもの |
| `{{EX2_TITLE}}` / `{{EX2_BODY}}` | 例② | 同上 |
| `{{SUMMARY}}` | まとめ（黄コールアウト内） | 1〜2文でまとめ |
| `{{PREV}}` | 前の用語ファイル名 | `prompt-injection.html` |
| `{{PREV_LABEL}}` | 前の用語表示名 | `プロンプトインジェクション` |
| `{{NEXT}}` | 次の用語ファイル名 | `jailbreak.html` |
| `{{NEXT_LABEL}}` | 次の用語表示名 | `次：ジェイルブレイク →` |

### 2. プレースホルダを埋める（Python例）

```python
with open('scripts/detail-page-template.html') as f:
    tpl = f.read()

data = {
    'NUM': '86',
    'CAT': 'H',
    'CAT_LABEL': 'セキュリティ',
    'EN': 'Prompt Injection',
    'NAME': 'プロンプトインジェクション',
    # ... 以下同じく
}

out = tpl
for key, val in data.items():
    out = out.replace(f'{{{{{key}}}}}', val)

with open('glossary/prompt-injection.html', 'w') as f:
    f.write(out)
```

**重要**: `.format()` は使わないこと。CSS波括弧（`{ }`）と干渉する。必ず `.replace()`。

### 3. index.html 3箇所を更新

1. `ALL` フィルタのカウント +1
2. 該当カテゴリのカウント +1
3. カテゴリセクション内にカードを挿入

### 4. 前後ナビの繋ぎ直し

新用語の前後のページの `{{NEXT}}` / `{{PREV}}` も更新する。

---

## 例えの品質チェック

詳細ページを追加したあと：

```bash
python3 scripts/audit-examples.py
```

を走らせると `examples-audit.md` が更新されて、新しい例えが既存とどう並ぶかが見える。

**「身近」の判定基準**: 「小学生でも家族でも通じるか？」

避けるべき例え：
- 業界用語（編集プロダクション、CVR 等）
- 年代依存（書留、ダイヤル錠、型紙 等）
- 技術用語そのもの（API、HTTP、USB-C 等）

---

## アニメーションのルール

ヒーローアニメは **CSS のみで自動ループ** を基本とする。

JSが必要な複雑なものは、`btn.addEventListener('click', play);` ではなく以下の自動発火パターンで書く：

```js
async function autoLoop() {
    await play();
    setTimeout(autoLoop, 2500);
}
setTimeout(autoLoop, 800);
```

再生ボタンは `style="display:none"` で非表示化する（過去のA/B/C互換のため残してある）。

---

## 色・フォント

詳細ページで使える色は DESIGN.md のデザイントークンだけ：
- `--ink` / `--ink-warm` / `--ink-soft` / `--ink-mute`
- `--bg` / `--bg-warm` / `--surface`
- `--mark`（黄色アクセント、多用禁物）
- `--line`

それ以外の色を追加する場合は DESIGN.md 側も更新すること。
