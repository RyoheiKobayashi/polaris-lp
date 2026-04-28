"""Generate OGP images for polaris-lp.

Brand-consistent (Notion light + yellow marker accent).
3 category images, each 1200x630 PNG.

Output:
    ../images/ogp-glossary.png   (AI / glossary/)
    ../images/ogp-contents.png   (Sales / contents/)
    ../images/ogp-learning.png   (Learning / learning/)

Usage:
    python3 scripts/generate-ogp.py
"""

from dataclasses import dataclass
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / "images"

W, H = 1200, 630

BG_WARM = (247, 246, 243)
INK = (25, 25, 25)
INK_WARM = (55, 53, 47)
INK_SOFT = (120, 119, 116)
INK_MUTE = (155, 154, 151)
LINE = (233, 233, 231)
MARK = (253, 236, 200)

FONT_SERIF = "/System/Library/Fonts/Supplemental/Baskerville.ttc"
FONT_SANS_JP = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_MONO = "/System/Library/Fonts/Supplemental/Courier New Bold.ttf"


@dataclass
class Category:
    filename: str
    top_label: str       # "AI  ·  VISUAL  GLOSSARY"
    subtitle: str        # "AIの単語"


CATEGORIES = [
    Category("ogp-glossary.png", "AI  ·  VISUAL  GLOSSARY", "AIの単語"),
    Category("ogp-contents.png", "SALES  ·  VISUAL  GLOSSARY", "コンテンツ販売の単語"),
    Category("ogp-learning.png", "LEARNING  ·  VISUAL  GLOSSARY", "学習方法の単語"),
]


def load(path: str, size: int, index: int = 0) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size, index=index)


def measure(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> tuple[int, int, int, int]:
    return draw.textbbox((0, 0), text, font=font)


def render(category: Category) -> None:
    img = Image.new("RGB", (W, H), BG_WARM)
    draw = ImageDraw.Draw(img)

    inset = 40
    draw.rectangle([inset, inset, W - inset, H - inset], outline=LINE, width=1)

    # 左上: AI · VISUAL GLOSSARY
    label_font = load(FONT_MONO, 22)
    draw.text((80, 70), category.top_label, font=label_font, fill=INK_SOFT)

    # 中央上: 知ってる言葉でわかる（serif italic、黄色マーカー）
    headline_font = load(FONT_SERIF, 110, index=1)
    headline = "知ってる言葉でわかる"
    # 日本語をBaskervilleで描けないので、Hiraginoのserif代用としてHiragino Sansを使用（serifではないがサイズで重みを出す）
    headline_font_jp = load(FONT_SANS_JP, 110)
    hb = measure(draw, headline, headline_font_jp)
    hw, hh = hb[2] - hb[0], hb[3] - hb[1]
    hx = (W - hw) // 2
    hy = 220

    # マーカーは「知ってる言葉」部分（最初の6文字）
    marker_text = "知ってる言葉"
    mb = measure(draw, marker_text, headline_font_jp)
    mw = mb[2] - mb[0]
    marker_x1 = hx
    marker_x2 = hx + mw
    marker_y1 = hy + int(hh * 0.55)
    marker_y2 = hy + hh + 12
    draw.rectangle([marker_x1, marker_y1, marker_x2, marker_y2], fill=MARK)
    draw.text((hx, hy), headline, font=headline_font_jp, fill=INK)

    # サブ: 「AIの単語」など
    sub_font = load(FONT_SANS_JP, 60)
    sb = measure(draw, category.subtitle, sub_font)
    sw, sh = sb[2] - sb[0], sb[3] - sb[1]
    sx = (W - sw) // 2
    sy = hy + hh + 60
    draw.text((sx, sy), category.subtitle, font=sub_font, fill=INK_WARM)

    # 右下: polaris-app.jp
    domain_font = load(FONT_MONO, 22)
    domain_text = "polaris-app.jp"
    db = measure(draw, domain_text, domain_font)
    dw, dh = db[2] - db[0], db[3] - db[1]
    draw.text((W - 80 - dw, H - 70 - dh), domain_text, font=domain_font, fill=INK_MUTE)

    out = IMG_DIR / category.filename
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG", optimize=True)
    print(f"Wrote {out} ({img.size[0]}x{img.size[1]})")


def main() -> None:
    for cat in CATEGORIES:
        render(cat)

    # 旧single-image版が残っていれば削除
    legacy = IMG_DIR / "ogp-default.png"
    if legacy.exists():
        legacy.unlink()
        print(f"Removed legacy {legacy}")


if __name__ == "__main__":
    main()
