"""Devpost image gallery: each figure padded to 3:2 (1800x1200) with a title bar, plus captions.md."""
import os
import shutil

from PIL import Image, ImageDraw, ImageFont

ROOT = "/Volumes/2TB/eurekadev"
OUT = f"{ROOT}/submission/gallery"
W, H, BAR = 1800, 1200, 120
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

ITEMS = [
    ("02_results.png", "fig4_cross_validation.png", "42–67% more expected survival than the standard model",
     "Out-of-sample survival gain for 10–200 AEDs, five temporal folds, 95% address-clustered bootstrap bands. "
     "Dashed: the same model with AEDs in 24/7 outdoor cabinets."),
    ("03_opening_hours.png", "fig5_opening_hours.png", "Ignoring opening hours overstates benefit by 67–106%",
     "Left: what an hours-blind plan promises vs. what it delivers. Right: benefit by time of day — "
     "indoor AEDs are almost useless between midnight and 6 a.m."),
    ("04_reach_cabinets.png", "fig8_reach_cabinets.png", "An AED loses half its value within ~123 m",
     "Left: the derived reach curve (survival model x real EMS delays). Right: 25 outdoor 24/7 cabinets "
     "deliver as much as 50 indoor AEDs."),
    ("05_map.png", "fig3_map.png", "Where the AEDs go: classic model vs. ours",
     "50 AED sites from each method, trained on 2017–18. Dots are cardiac arrests colored by EMS response time; "
     "shading is the CDC Social Vulnerability Index."),
    ("06_fairness.png", "fig6_fairness.png", "Fairness is cheap, but full parity is impossible",
     "Left: in-sample price of fairness. Right: a fairness floor lifts the worst-served group with no "
     "detectable out-of-sample cost."),
    ("07_robustness.png", "fig7_sensitivity.png", "Holds in all 30 robustness checks",
     "Advantage over the classic model under 10 alternative assumptions at 3 budgets "
     "(95% address-clustered bootstrap intervals)."),
    ("08_prototype.png", "fig9_prototype.png", "AED Placement Explorer (interactive prototype)",
     "Add AEDs one at a time and switch between indoor sites, 24/7 cabinets and the classic model."),
]


def pad(src, title):
    im = Image.open(src).convert("RGB")
    canvas = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([0, 0, W, BAR], fill="#0d1321")
    font = ImageFont.truetype(FONT, 46)
    tw = draw.textlength(title, font=font)
    draw.text(((W - tw) / 2, (BAR - 52) / 2), title, fill="#f4f1ea", font=font)
    box_w, box_h = W - 80, H - BAR - 60
    scale = min(box_w / im.width, box_h / im.height)
    im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    canvas.paste(im, ((W - im.width) // 2, BAR + 30 + (box_h - im.height) // 2))
    return canvas


os.makedirs(OUT, exist_ok=True)
shutil.copy(f"{ROOT}/submission/thumbnail.png", f"{OUT}/01_thumbnail.png")
lines = ["# Devpost image gallery\n",
         "Upload in this order. Each image is 1800x1200 (3:2), well under 5 MB.\n",
         "| File | Caption |", "|---|---|",
         "| 01_thumbnail.png | Where Should the Defibrillators Go? Optimizing public AED placement from 2,706 "
         "real cardiac arrests in Virginia Beach. |"]
for name, fig, title, caption in ITEMS:
    pad(f"{ROOT}/figures/{fig}", title).save(f"{OUT}/{name}", optimize=True)
    lines.append(f"| {name} | **{title}.** {caption} |")
open(f"{OUT}/captions.md", "w").write("\n".join(lines) + "\n")
for f in sorted(os.listdir(OUT)):
    print(f, os.path.getsize(f"{OUT}/{f}") // 1024, "KB")
