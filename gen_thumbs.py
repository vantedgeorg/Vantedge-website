"""Make Research page covers from report PDFs.

For every PDF in static/reports/ without a cover yet, render page 1 and save a small
JPEG to static/v2/covers/<pdf name>.jpg (the Research cards show it at 168x238).

Needs: pip install pdf2image pillow, plus Poppler installed (set POPPLER_PATH on Windows).
Run from the project folder:  python gen_thumbs.py
"""
import os
from pdf2image import convert_from_path

INPUT_DIR = "static/reports"
OUTPUT_DIR = "static/v2/covers"
POPPLER_PATH = os.environ.get("POPPLER_PATH")  # e.g. C:\...\poppler\Library\bin on Windows

os.makedirs(OUTPUT_DIR, exist_ok=True)

for filename in sorted(os.listdir(INPUT_DIR)):
    if not filename.endswith(".pdf"):
        continue
    out_path = os.path.join(OUTPUT_DIR, filename[:-4] + ".jpg")
    if os.path.exists(out_path):
        continue
    print(f"Making cover for {filename}...")
    try:
        page = convert_from_path(os.path.join(INPUT_DIR, filename), dpi=72,
                                 first_page=1, last_page=1, poppler_path=POPPLER_PATH)[0]
        page.thumbnail((336, 952))
        w, h = page.size
        page.crop((0, 0, w, min(h, int(w * 238 / 168)))).convert("RGB").save(out_path, "JPEG", quality=85)
    except Exception as e:
        print(f"  Error: {e}")

print("Done.")
