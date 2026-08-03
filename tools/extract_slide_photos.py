#!/usr/bin/env python3
"""Ambil bagian FOTO dari slide Instagram yang udah jadi, buang panel teksnya.

Slide lama = foto di atas + panel terang berisi teks di bawah. Script ini
nyari di mana panel terang itu mulai, terus motong tepat di atas gradasinya,
jadi fotonya bisa dipakai ulang buat copy baru.

  python3 tools/extract_slide_photos.py <folder-slide> -o <folder-output>
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

# Panel terang di slide Parameter warnanya sekitar (241,242,244).
PANEL_MIN_BRIGHTNESS = 232
PANEL_MAX_SPREAD = 14  # baris panel hampir rata warnanya


def row_is_panel(pixels, w: int, y: int) -> bool:
    """True kalau baris ini terang dan rata — ciri panel teks."""
    samples = [pixels[x, y] for x in range(0, w, max(w // 48, 1))]
    lo = min(min(p) for p in samples)
    hi = max(max(p) for p in samples)
    return lo >= PANEL_MIN_BRIGHTNESS and (hi - lo) <= PANEL_MAX_SPREAD


def find_panel_top(img: Image.Image) -> int:
    """Cari baris paling atas dari blok panel yang nyambung sampai bawah."""
    w, h = img.size
    px = img.load()
    y = h - 1
    if not row_is_panel(px, w, y):
        return h  # nggak ada panel; pakai gambar utuh
    while y > int(h * 0.35) and row_is_panel(px, w, y - 1):
        y -= 1
    return y


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("src", type=Path, help="folder berisi slide PNG")
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument(
        "--fade",
        type=float,
        default=0.085,
        help="porsi tinggi gambar di atas panel yang ikut dibuang (gradasi)",
    )
    args = ap.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    files = sorted(p for p in args.src.glob("*.png"))
    if not files:
        raise SystemExit(f"Nggak ada PNG di {args.src}")

    for path in files:
        img = Image.open(path).convert("RGB")
        panel_top = find_panel_top(img)
        cut = max(int(panel_top - img.height * args.fade), int(img.height * 0.3))
        img.crop((0, 0, img.width, cut)).save(args.out / path.name, "PNG", optimize=True)
        pct = 100 * cut / img.height
        print(f"  {path.name}: panel di {panel_top}px, dipotong di {cut}px ({pct:.0f}%)")

    print(f"\n{len(files)} foto -> {args.out}")


if __name__ == "__main__":
    main()
