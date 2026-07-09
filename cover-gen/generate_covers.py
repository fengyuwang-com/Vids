#!/usr/bin/env python3
"""封面生成器 — 一套文案，同时出 B站(16:9) + 抖音(3:4) 两套炸裂封面。

用法:
  python generate_covers.py                  # 同时出两套
  python generate_covers.py --landscape      # 仅 B站 16:9
  python generate_covers.py --portrait       # 仅 抖音 3:4

依赖:
  pip install playwright
  playwright install chromium
"""

import argparse, os, sys
from pathlib import Path

# ============================================================
#  配置 — 可被外部 import 复用
# ============================================================

OUT_DIR = Path(__file__).resolve().parent.parent / "VideoToEdit"

# 照片来源目录
PHOTO_DIRS = [
    Path(__file__).resolve().parent.parent / "assets" / "leijun_photos",
    Path(__file__).resolve().parent.parent / "assets" / "leijun_photos2",
]

# 所有封面文案
# file 字段自动从 id + big 生成，可手动覆盖
COVERS = [
    {
        "id": "01",
        "big": "为什么总被骂？",
        "mid": "爱恨同源",
        "sub": "容错率≈0 · 全网都在骂是幻觉？",
        "badge": "5个真相",
        "bg": "#1a0000",
        "glow": "#ff2200",
    },
    {
        "id": "02",
        "big": "穿啥都被骂",
        "mid": "没衣服穿了",
        "sub": "雷布斯->雷斯克->雷仁勋 · 借来的符号",
        "badge": "标签陷阱",
        "bg": "#1a0a00",
        "glow": "#ff6600",
    },
    {
        "id": "03",
        "big": "热干面翻车",
        "mid": "亲民变KPI",
        "sub": "小女孩一句话戳破 · 流水线真诚",
        "badge": "翻车现场",
        "bg": "#1a0500",
        "glow": "#ff4400",
    },
    {
        "id": "04",
        "big": "手机能蒙",
        "mid": "汽车蒙不过去",
        "sub": "4.2万碳盖 · 庭审不算数 · 小字的代价",
        "badge": "安全诚信",
        "bg": "#000a1a",
        "glow": "#0066ff",
    },
    {
        "id": "05",
        "big": "押上全部声誉",
        "mid": "他退不了",
        "sub": "被黑怕了 · 神像与囚笼 · 没有人能接班",
        "badge": "终极困局",
        "bg": "#0a001a",
        "glow": "#8800ff",
    },
]

# 自动补充 file 字段
for _c in COVERS:
    _c.setdefault("file", f"{_c['id']}-封面-{_c['big']}")

# ============================================================
#  字号计算引擎
# ============================================================

def calc_sizes(text_big, text_mid, text_sub, safe_width):
    """根据安全宽度动态计算三行文字的字号和字距。"""

    def _size(text, cap, minimum):
        n = max(len(text), 1)
        return int(min(cap, max(minimum, safe_width / n)))

    def _ls(text, font_sz, default):
        n = len(text)
        used = n * font_sz
        room = safe_width - used
        if room > 120:
            return default
        elif room > 40:
            return max(2, default - 2)
        else:
            return 1

    big_sz = _size(text_big, 220, 140)
    mid_sz = _size(text_mid, 140, 80)
    sub_sz = _size(text_sub, 55, 30)

    return {
        "big_sz": big_sz,
        "big_ls": _ls(text_big, big_sz, 4),
        "mid_sz": mid_sz,
        "mid_ls": _ls(text_mid, mid_sz, 6),
        "sub_sz": sub_sz,
        "sub_ls": _ls(text_sub, sub_sz, 3),
    }

# ============================================================
#  HTML 渲染
# ============================================================

def _html(c, photo_uri, sz, w, h):
    """产生单张封面 HTML。w×h 控制输出比例（16:9 或 3:4）。"""
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:{w}px; height:{h}px; overflow:hidden; }}
body {{
    background: {c['bg']};
    font-family: "Microsoft YaHei", "SimHei", "PingFang SC", "Noto Sans SC", sans-serif;
    position: relative;
}}

/* 背景照片 */
.photo-bg {{
    position: absolute; inset: 0;
    background-image: url('{photo_uri}');
    background-size: cover;
    background-position: center 30%;
    opacity: 0.72;
}}

/* 暗角 */
.vignette {{
    position: absolute; inset: 0;
    background: radial-gradient(ellipse at center, transparent 25%, #000 100%);
}}

/* 爆炸放射光 */
.burst {{
    position: absolute; inset: 0; z-index: 1;
    background: conic-gradient(from 0deg at 50% 50%,
        transparent 0deg, {c['glow']}15 10deg, transparent 20deg,
        transparent 40deg, {c['glow']}0a 50deg, transparent 60deg,
        transparent 80deg, {c['glow']}15 90deg, transparent 100deg,
        transparent 120deg, {c['glow']}0a 130deg, transparent 140deg,
        transparent 160deg, {c['glow']}15 170deg, transparent 180deg,
        transparent 200deg, {c['glow']}0a 210deg, transparent 220deg,
        transparent 240deg, {c['glow']}15 250deg, transparent 260deg,
        transparent 280deg, {c['glow']}0a 290deg, transparent 300deg,
        transparent 320deg, {c['glow']}15 330deg, transparent 340deg);
}}

/* 中心光晕 */
.glow {{
    position: absolute; top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: min({w}px, 900px); height: min({w}px, 900px);
    border-radius: 50%;
    background: radial-gradient(circle, {c['glow']}44 0%, transparent 70%);
    z-index: 1;
}}

/* 金色装饰角 */
.corner {{ position: absolute; z-index: 5; width: min({w}*0.07, 130px); height: min({w}*0.07, 130px); opacity: 0.85; }}
.corner::before {{
    content: ''; position: absolute;
    width: 100%; height: 100%;
}}
.corner-tl {{ top: 30px; left: 30px; }}
.corner-tl::before {{
    border-top: 4px solid #ffdd00;
    border-left: 4px solid #ffdd00;
    box-shadow: -4px -4px 20px {c['glow']}66;
}}
.corner-tr {{ top: 30px; right: 30px; }}
.corner-tr::before {{
    border-top: 4px solid #ffdd00;
    border-right: 4px solid #ffdd00;
    box-shadow: 4px -4px 20px {c['glow']}66;
}}
.corner-bl {{ bottom: 40px; left: 30px; }}
.corner-bl::before {{
    border-bottom: 4px solid #ffdd00;
    border-left: 4px solid #ffdd00;
    box-shadow: -4px 4px 20px {c['glow']}66;
}}
.corner-br {{ bottom: 40px; right: 30px; }}
.corner-br::before {{
    border-bottom: 4px solid #ffdd00;
    border-right: 4px solid #ffdd00;
    box-shadow: 4px 4px 20px {c['glow']}66;
}}
.corner::after {{
    content: ''; position: absolute;
    width: 10px; height: 10px;
    background: #ffdd00;
    box-shadow: 0 0 20px #ffdd00aa;
}}
.corner-tl::after {{ top: -5px; left: -5px; }}
.corner-tr::after {{ top: -5px; right: -5px; }}
.corner-bl::after {{ bottom: -5px; left: -5px; }}
.corner-br::after {{ bottom: -5px; right: -5px; }}

/* 文字层 — 居中 */
.text-layer {{
    position: absolute; z-index: 4;
    width: 100%; text-align: center;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    padding: 0 max(30px, {w}*0.025);
}}

/* 标签 */
.badge {{
    display: inline-block;
    background: {c['glow']};
    color: #fff;
    font-size: 34px; font-weight: 900;
    padding: 10px 40px;
    border-radius: 6px;
    margin-bottom: max(12px, {w}*0.012);
    letter-spacing: 8px;
    box-shadow: 0 4px 30px rgba(0,0,0,0.8);
}}

/* 大字 */
.big-text {{
    font-size: {sz['big_sz']}px; font-weight: 900;
    color: #ffdd00;
    line-height: 1.1;
    letter-spacing: {sz['big_ls']}px;
    text-shadow:
        -10px -10px 0 #000,
         10px -10px 0 #000,
        -10px  10px 0 #000,
         10px  10px 0 #000,
        -6px   0    0 #000,
         6px   0    0 #000,
         0   -6px   0 #000,
         0    6px   0 #000,
        0 0 50px rgba(0,0,0,0.95),
        0 0 100px {c['glow']}44;
    margin-bottom: 8px;
}}

/* 中字 */
.mid-text {{
    font-size: {sz['mid_sz']}px; font-weight: 900;
    color: #ff6600;
    line-height: 1.15;
    letter-spacing: {sz['mid_ls']}px;
    text-shadow:
        -6px -6px 0 #000,
         6px -6px 0 #000,
        -6px  6px 0 #000,
         6px  6px 0 #000,
        0 0 30px rgba(0,0,0,0.85),
        0 0 60px #ff660066;
    margin-bottom: 6px;
}}

/* 分割线 */
.divider {{
    width: min(300px, 25%);
    height: 3px;
    margin: 0 auto max(6px, 0.6vw) auto;
    background: linear-gradient(90deg, transparent, {c['glow']}88, #ffdd00aa, {c['glow']}88, transparent);
    box-shadow: 0 0 20px {c['glow']}44;
    border-radius: 2px;
}}

/* 小字 */
.sub-text {{
    font-size: {sz['sub_sz']}px; font-weight: 800;
    color: #ffcc00;
    line-height: 1.2;
    letter-spacing: {sz['sub_ls']}px;
    text-shadow:
        -4px -4px 0 #000,
         4px -4px 0 #000,
        -4px  4px 0 #000,
         4px  4px 0 #000,
        0 0 20px rgba(0,0,0,0.95);
}}

/* 底部光带 */
.stripe {{
    position: absolute; bottom: 0; left: 0; right: 0;
    height: 8px;
    background: linear-gradient(90deg, {c['glow']}, #ffdd00, {c['glow']});
    z-index: 5;
}}
</style>
</head><body>
<div class="photo-bg"></div>
<div class="vignette"></div>
<div class="burst"></div>
<div class="glow"></div>

<div class="corner corner-tl"></div>
<div class="corner corner-tr"></div>
<div class="corner corner-bl"></div>
<div class="corner corner-br"></div>

<div class="text-layer">
    <div class="badge">{c['badge']}</div>
    <div class="big-text">{c['big']}</div>
    <div class="divider"></div>
    <div class="mid-text">{c['mid']}</div>
    <div class="sub-text">{c['sub']}</div>
</div>

<div class="stripe"></div>
</body></html>"""


def _best_photo():
    """从所有照片目录中选取文件最大的那张。"""
    photos = []
    for d in PHOTO_DIRS:
        if d.is_dir():
            photos.extend(d.glob("*.jpg"))
    if not photos:
        photos.extend(d.glob("*.png") for d in PHOTO_DIRS if d.is_dir())
        photos = [p for sub in photos for p in sub]
    if not photos:
        print("ERROR: No photo found!")
        sys.exit(1)
    photos.sort(key=lambda f: f.stat().st_size, reverse=True)
    return str(photos[0])


def generate_cover(c, photo_uri, width, height, suffix=""):
    """生成一张封面并保存为 JPG。

    Args:
        c: 封面数据 dict
        photo_uri: 照片 file:// URI
        width, height: 画布尺寸（px）
        suffix: 文件名后缀，如 "-抖音"
    Returns:
        输出文件路径
    """
    # B站 16:9 大封面的小图展示是 4:3 居中裁剪（1440x1080）
    # 所以 16:9 横版用 1420 安全宽（4:3 可见区 1440 - 描边余量）
    # 抖音 3:4 竖版用全宽 - 60（无后续裁剪）
    safe_w = 1420 if width > height else width - 60
    sz = calc_sizes(c["big"], c["mid"], c["sub"], safe_w)

    from playwright.sync_api import sync_playwright

    html = _html(c, photo_uri, sz, width, height)
    base = c["file"].rsplit(".", 1)[0]
    fname = f"{base}{suffix}.jpg"
    out = OUT_DIR / fname

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height})
        tmp_html = OUT_DIR / f"._{fname}.html"
        tmp_html.write_text(html, encoding="utf-8")
        page.goto(tmp_html.as_uri(), wait_until="networkidle")
        page.wait_for_timeout(2000)
        page.screenshot(path=str(out), full_page=False, type="jpeg", quality=97)
        page.close()
        browser.close()
        tmp_html.unlink(missing_ok=True)

    kb = os.path.getsize(out) // 1024
    print(f"  [{c['id']}] big={c['big']} => {sz['big_sz']}px | {fname} ({kb} KB)")
    return out


# ============================================================
#  CLI
# ============================================================

def main():
    ap = argparse.ArgumentParser(description="炸裂封面生成器 — B站 16:9 + 抖音 3:4")
    ap.add_argument("--landscape", action="store_true", help="仅生成 B站 16:9 横版")
    ap.add_argument("--portrait", action="store_true", help="仅生成 抖音 3:4 竖版")
    args = ap.parse_args()

    do_landscape = not args.portrait or args.landscape
    do_portrait = not args.landscape or args.portrait

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    photo = _best_photo()
    photo_uri = Path(photo).resolve().as_uri()
    print(f"Photo: {photo} ({os.path.getsize(photo)//1024} KB)")

    if do_landscape:
        print("\n--- B站 16:9 横版封面 ---")
        for c in COVERS:
            generate_cover(c, photo_uri, 1920, 1080)

    if do_portrait:
        print("\n--- 抖音 3:4 竖版封面 ---")
        for c in COVERS:
            generate_cover(c, photo_uri, 1080, 1440, suffix="-抖音")

    print(f"\nDone! Output: {OUT_DIR}")


if __name__ == "__main__":
    main()
