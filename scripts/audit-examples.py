#!/usr/bin/env python3
"""
身近な例え 監査スクリプト

glossary/*.html から「身近な例えで理解する」セクションを抽出し、
examples-audit.md に整形出力する。

使い方:
    python3 scripts/audit-examples.py
"""

import re
import glob
import html
import os
from collections import defaultdict, Counter

ROOT = os.path.join(os.path.dirname(__file__), '..')
GLOSSARY_DIR = os.path.join(ROOT, 'glossary')
OUTPUT = os.path.join(ROOT, 'examples-audit.md')

CATEGORY_LABELS = {
    'A': 'AIの基本概念',
    'B': 'プロンプトエンジニアリング',
    'C': 'ナレッジ・AI活用の仕組み',
    'D': 'AIツール・サービス',
    'E': 'Claude Code関連',
    'G': 'エンジニアリング',
    'H': 'セキュリティ',
}

DOMAINS = {
    '🏠 家・家事': ['家の', '家に', '合鍵', '玄関', '冷蔵庫', '家電', '部屋', '鍵', '家事', 'マット', '金庫'],
    '🍜 食・飲食': ['ラーメン', '料理', 'レシピ', 'レストラン', 'キッチン', '味見', '食堂', '料亭', '食べ歩', 'カレー', 'じゃがいも', '玉ねぎ', '食材', '料理人', 'お客さん', 'コック'],
    '🚗 交通・乗り物': ['車', '新幹線', 'バス', '電車', 'カメラ', '飛行機', 'F1', 'マニュアル', 'オートマ'],
    '🎓 学校・勉強': ['学校', '授業', '教科書', '試験', '先生', '生徒', '塾', 'ノート', '論文', '学術', '目次', '脚注'],
    '📱 スマホ・日常IT': ['スマホ', 'iPhone', 'アプリ', 'LINE', 'メール', 'Google検索', '予測変換', 'Siri', 'ボイスメモ', 'タブ', '目覚まし'],
    '👔 仕事・職場': ['会議', '秘書', 'マニュアル', '新入社員', '上司', '部下', '同僚', '編集者', '編集長', 'ライター', 'リサーチ', 'アシスタント', '社員'],
    '👨\u200d👩\u200d👧 家族・人間関係': ['家族', '友人', '友達', '子供', '親', '奥さん', '旦那', '夫婦'],
    '🏪 お店・サービス': ['コンビニ', 'ウェイター', '店員', '宅配便', 'お店', '不在通知', 'レシピ本', '職人'],
    '📺 メディア・娯楽': ['本', 'テレビ', 'ラジオ', '雑誌', '映画', '辞書', '百科事典', '書', '本を一冊', 'iTunes'],
    '💰 お金・決済': ['銀行', 'クレジット', '請求', '引き落とし', '支払い', '電話料金', 'お会計', 'サブスク'],
    '⚙️ 業界・技術': ['API', 'プログラミング', '編集プロダクション', 'エンジニア', 'データベース', 'サーバー', 'コード', 'エンジン', 'USB-C', 'HTTP', 'HACCP'],
    '🏗️ 建築・工事': ['家を建て', '建築', '設計図', '骨組み', '模型', '工場', '大工'],
    '🚨 法律・警察': ['刑務所', '脱獄', '警察', '法律', '逮捕', '空港', '検問', '書留', '普通郵便'],
    '🔐 鍵・鍵っ子': [],  # 家と被るので無効化
    '📦 物理モノ': ['鎖', '檻', 'ダイヤル錠', 'パズル', '型紙', '模型', '回転扉', '自動ドア'],
}

# 弱い候補マーカー
WEAK_KEYWORDS = {
    '業界用語': ['編集プロダクション', 'SES', 'ファネル', 'CVR', 'LTV', 'HACCP', 'COPPA', 'OAuth', 'Docker'],
    '年代依存の可能性': ['書留', '普通郵便', '手紙', '電報', 'ダイヤル錠', '口述筆記', '型紙', '文字起こし業者'],
    '技術寄り・AI者限定': ['HTTP', 'API', 'HTTPS', 'エンジン', 'USB-C', 'コンパイラ'],
}


def classify_domain(text: str) -> str:
    """本文からドメインを判定。複数マッチしたら最多キーワードの方を採用。"""
    scores = Counter()
    for domain, kws in DOMAINS.items():
        for kw in kws:
            if kw and kw in text:
                scores[domain] += 1
    if not scores:
        return '❓ その他'
    return scores.most_common(1)[0][0]


def detect_weak(text: str) -> list:
    """弱いマーカーを検出して、理由リストを返す。"""
    reasons = []
    for reason, kws in WEAK_KEYWORDS.items():
        for kw in kws:
            if kw in text:
                reasons.append(f'{reason}: "{kw}"')
                break  # 同じ理由で複数検出はしない
    return reasons


def clean_text(raw: str) -> str:
    """HTMLタグ除去・空白整形。"""
    # <br>を改行に（でも最終的に1行化するため消す）
    t = re.sub(r'<br\s*/?>', ' ', raw)
    # すべてのタグ除去
    t = re.sub(r'<[^>]+>', '', t)
    # html entity
    t = html.unescape(t)
    # 連続空白を1つに
    t = re.sub(r'\s+', ' ', t).strip()
    return t


def extract_page(path: str) -> dict:
    """1ファイルから情報抽出。"""
    with open(path) as f:
        content = f.read()

    # 番号・カテゴリ: "XX · [A-H]. XXX" のような cat-label
    m = re.search(r'cat-label[^>]*>\s*(\d+)\s*·\s*([A-H])\.\s*[^<]+<', content)
    if not m:
        return None
    num = int(m.group(1))
    cat = m.group(2)

    # タイトル h1
    m = re.search(r'<h1[^>]*>([\s\S]*?)</h1>', content)
    title = clean_text(m.group(1)) if m else '(title missing)'

    # 「身近な例えで理解する」セクションを抽出
    m = re.search(
        r'身近な例えで理解する[\s\S]*?(?=<(?:section|div)\s+class="callout)',
        content
    )
    if not m:
        return None
    section = m.group(0)

    # card p-6 を全部拾う
    cards = re.findall(
        r'<div class="card p-6">([\s\S]*?)</div>\s*(?=<div class="card p-6">|</div>\s*</section>|</div>\s*</div>)',
        section
    )

    # card抽出が不安定な場合、もっとシンプルに
    if len(cards) < 2:
        cards = re.findall(r'<div class="card p-6">([\s\S]*?)</div>\s*</div>\s*<', section)
    if len(cards) < 2:
        # 最終手段：h3直後のp
        cards = re.findall(r'(<h3[\s\S]*?</p>)', section)[:2]

    examples = []
    for card in cards[:2]:
        ht = re.search(r'<h3[^>]*>([\s\S]*?)</h3>', card)
        hp = re.search(r'<p[^>]*>([\s\S]*?)</p>', card)
        if not ht or not hp:
            continue
        etitle = clean_text(ht.group(1))
        ebody = clean_text(hp.group(1))
        examples.append({'title': etitle, 'body': ebody})

    return {
        'num': num,
        'cat': cat,
        'title': title,
        'file': os.path.basename(path),
        'examples': examples,
    }


def main():
    files = sorted(glob.glob(os.path.join(GLOSSARY_DIR, '*.html')))
    # index.html / disclaimer.html は除外
    files = [f for f in files if os.path.basename(f) not in ('index.html', 'disclaimer.html')]

    pages = []
    for f in files:
        p = extract_page(f)
        if p:
            pages.append(p)
        else:
            print(f'[skip] {f}: structure not matched')

    # カテゴリ・番号順にソート
    pages.sort(key=lambda x: (x['cat'], x['num']))

    # ドメイン集計
    domain_counter = Counter()
    weak_list = []

    # 出力組み立て
    out = []
    out.append('# 身近な例え 監査')
    out.append('')
    out.append(f'全{len(pages)}用語 × 例え2本 = {len(pages) * 2}件を棚卸し。')
    out.append('判定基準：「小学生でも家族でも通じるか？」')
    out.append('')
    out.append('## 判定ドメイン')
    for d in list(DOMAINS.keys()) + ['❓ その他']:
        out.append(f'- {d}')
    out.append('')
    out.append('---')
    out.append('')

    # カテゴリごと
    by_cat = defaultdict(list)
    for p in pages:
        by_cat[p['cat']].append(p)

    for cat in sorted(by_cat.keys()):
        label = CATEGORY_LABELS.get(cat, '?')
        out.append(f'## Category {cat}: {label}（{len(by_cat[cat])}用語）')
        out.append('')
        for p in by_cat[cat]:
            out.append(f"### {p['num']:02d}. {p['title']}（{p['file']}）")
            for i, ex in enumerate(p['examples'], 1):
                domain = classify_domain(ex['title'] + ' ' + ex['body'])
                domain_counter[domain] += 1
                weak = detect_weak(ex['title'] + ' ' + ex['body'])
                weak_tag = ' ⚠️' if weak else ''
                out.append(f"- {domain}{weak_tag} | {ex['title']}")
                if weak:
                    for w in weak:
                        out.append(f"  - 🔴 {w}")
                        weak_list.append({
                            'term': p['title'],
                            'file': p['file'],
                            'example_title': ex['title'],
                            'reason': w,
                        })
            out.append('')
        out.append('')

    # ドメイン集計
    out.append('---')
    out.append('')
    out.append('## ドメイン別集計')
    out.append('')
    total = sum(domain_counter.values())
    for domain, count in domain_counter.most_common():
        pct = (count / total * 100) if total else 0
        out.append(f'- {domain}: **{count}件** ({pct:.1f}%)')
    out.append('')

    # 弱い例え
    out.append('---')
    out.append('')
    out.append(f'## ⚠️ 弱い例え候補（自動判定 {len(weak_list)}件）')
    out.append('')
    out.append('自動判定は業界用語・年代依存・技術寄りキーワードで検出。最終判断は人間。')
    out.append('')
    if not weak_list:
        out.append('（自動検出なし）')
    else:
        for w in weak_list:
            out.append(f"- **{w['term']}** ｜ {w['example_title']}")
            out.append(f"  - → {w['reason']}")
            out.append(f"  - file: `glossary/{w['file']}`")
    out.append('')

    # 未使用ドメイン
    used = set(domain_counter.keys())
    all_domains = set(list(DOMAINS.keys()) + ['❓ その他'])
    unused = all_domains - used
    out.append('---')
    out.append('')
    out.append('## 未使用ドメイン（次の用語で活用余地あり）')
    out.append('')
    if not unused:
        out.append('（全ドメイン使用済み）')
    else:
        for d in sorted(unused):
            out.append(f'- {d}')
    out.append('')

    # フッター
    out.append('---')
    out.append('')
    out.append('※ このファイルは `scripts/audit-examples.py` の自動生成結果です。')
    out.append('  編集しても次回実行で上書きされます。書き直したい例えは元のHTMLを修正してください。')

    with open(OUTPUT, 'w') as f:
        f.write('\n'.join(out) + '\n')

    print(f'✅ Generated {OUTPUT}')
    print(f'   {len(pages)} terms, {total} examples, {len(weak_list)} weak candidates')


if __name__ == '__main__':
    main()
