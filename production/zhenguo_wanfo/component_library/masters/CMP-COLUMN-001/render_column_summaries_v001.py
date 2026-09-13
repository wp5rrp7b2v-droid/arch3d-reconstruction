"""Render the two text review sheets from the committed parameter contract."""

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[5]
PARAMS = Path(__file__).with_name("CMP-COLUMN-001_MASTER_PARAMS_V001.json")
REVIEW = ROOT / "production/zhenguo_wanfo/review/P3_1/masters/CMP-COLUMN-001"
FONT = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"


def make_base(kicker, title, subtitle):
    im = Image.new("RGB", (1400, 1000), "#f7f7f5")
    d = ImageDraw.Draw(im)
    f_small = ImageFont.truetype(FONT, 27)
    f_medium = ImageFont.truetype(FONT, 35)
    f_large = ImageFont.truetype(FONT, 61)
    d.rectangle((0, 0, 1400, 18), fill="#626262")
    d.text((84, 62), kicker, font=f_small, fill="#666666")
    d.text((84, 116), title, font=f_large, fill="#222222")
    d.text((86, 205), subtitle, font=f_medium, fill="#555555")
    d.line((84, 276, 1316, 276), fill="#d7d7d5", width=3)
    d.text((84, 946), "CMP-COLUMN-001  /  MASTER V001  /  T-011 PILOT", font=f_small, fill="#777777")
    return im, d, f_small, f_medium


def card(draw, bounds, label, value, detail, fonts, accent="#727272"):
    small, medium = fonts
    x0, y0, x1, y1 = bounds
    draw.rounded_rectangle(bounds, radius=20, fill="white", outline="#dadad8", width=2)
    draw.rectangle((x0, y0, x0 + 11, y1), fill=accent)
    draw.text((x0 + 38, y0 + 25), label, font=small, fill="#666666")
    draw.text((x0 + 38, y0 + 72), value, font=ImageFont.truetype(FONT, 46), fill="#222222")
    draw.text((x0 + 38, y0 + 145), detail, font=small, fill="#666666")


def main():
    data = json.loads(PARAMS.read_text())
    p = {item["key"]: item for item in data["parameters"]}
    REVIEW.mkdir(parents=True, exist_ok=True)
    im, d, small, medium = make_base("GEOMETRY / PARAMETER", "柱身参考实现", "PARAMETRIC CIRCULAR COLUMN BODY  ·  mm")
    card(d, (84, 325, 672, 545), "DIAMETER  /  柱径", f'{p["diameter_mm"]["value"]:.1f} mm', "OBSERVED_Z001 · 现状约值", (small, medium), "#666666")
    card(d, (728, 325, 1316, 545), "BODY HEIGHT  /  柱身高", f'{p["height_mm"]["value"]:.1f} mm', "RC_Z006_RC_01 · 可替换候选", (small, medium), "#898989")
    d.text((86, 604), "LOCAL MASTER CONTRACT", font=medium, fill="#303030")
    lines = [
        "Origin: bottom-face center  ·  +Z: body axis / gravity up",
        "Location (0,0,0)  ·  Rotation (0,0,0)  ·  Scale (1,1,1)",
        "Body only: no taper, entasis, side-foot, base, capital or joinery",
        "Reference realization only; dimensions are parameter-driven",
    ]
    for n, line in enumerate(lines):
        d.text((90, 672 + n * 58), line, font=small, fill="#4c4c4c")
    im.save(REVIEW / "DIMENSION_PARAMETER_SUMMARY.png")

    im, d, small, medium = make_base("EVIDENCE / UNCERTAINTY", "证据边界", "Three separate meanings are preserved in this Master")
    diameter_detail = f'~{p["diameter_mm"]["value"]:.0f} mm report-adjusted current diameter; not an exact 963 design value'
    height_detail = f'{p["height_mm"]["value"]:.1f} mm = {data["height_candidate"]["multiplier"]} × MOD-006; production candidate, not proven 963 height'
    card(d, (84, 315, 1316, 515), "Z-001  ·  DIAMETER", "OBSERVED REFERENCE", diameter_detail, (small, medium), "#646464")
    card(d, (84, 533, 1316, 733), "Z-006-RC-01  ·  HEIGHT", "REPLACEABLE RC / D-023", height_detail, (small, medium), "#8c8c8c")
    d.rounded_rectangle((84, 752, 1316, 913), radius=20, fill="#ededeb")
    d.text((120, 775), "Z-006  =  UNKNOWN / null / DO_NOT_LOCK", font=medium, fill="#2e2e2e")
    d.text((120, 834), "HIS-002 = component originality unknown", font=small, fill="#474747")
    d.text((120, 874), "No claim of a verified 963 original column or exact historical body height.", font=small, fill="#474747")
    im.save(REVIEW / "EVIDENCE_UNCERTAINTY_SUMMARY.png")


if __name__ == "__main__":
    main()
