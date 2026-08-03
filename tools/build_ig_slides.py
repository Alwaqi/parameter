#!/usr/bin/env python3
"""Render slide carousel Instagram Parameter dari file JSON.

Foto (hasil generate AI, tanpa teks) ditaruh di dua per tiga atas; teksnya
di-render di sini biar hurufnya tajam dan copy-nya bisa direvisi tanpa
generate ulang gambar.

Pakai [kurung siku] di headline buat bagian yang diwarnai biru.

  python3 tools/build_ig_slides.py <slides.json> -o <folder-output>
  python3 tools/build_ig_slides.py <slides.json> -o <folder> --demo

--demo bikin background abu-abu (tanpa foto) buat ngecek layout tipografi.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONTS = Path("/Library/Fonts")
FONT_HEADLINE = FONTS / "Archivo_SemiCondensed-Black.ttf"
FONT_BOLD = FONTS / "Archivo-Bold.ttf"
FONT_SEMIBOLD = FONTS / "Archivo-SemiBold.ttf"

# Aset maskot Para: para-thinking / para-welcome / para-building
POSES = Path("public")

NAVY = (11, 23, 48)
BLUE = (27, 92, 255)
PANEL = (241, 242, 244)
INK_SOFT = (28, 40, 66)

# Proporsi kanvas 1080x1920; semua ukuran diskalakan dari sini.
BASE_W, BASE_H = 1080, 1920


class Layout:
    """Ukuran layout, diskalakan dari kanvas dasar 1080x1920."""

    def __init__(self, w: int, h: int):
        self.w, self.h = w, h
        s = w / BASE_W
        self.s = s
        self.margin = int(84 * s)
        self.panel_top = int(h * 0.655)
        self.fade = int(310 * s)
        self.kicker_size = int(30 * s)
        self.kicker_track = 3.0 * s
        self.headline_size = int(104 * s)
        self.headline_lead = 1.02
        self.sub_size = int(46 * s)
        self.handle_size = int(32 * s)
        self.gap_kicker = int(38 * s)
        self.gap_sub = int(34 * s)


def load_font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    if not path.exists():
        raise SystemExit(f"Font nggak ketemu: {path}")
    return ImageFont.truetype(str(path), size)


def text_width(draw: ImageDraw.ImageDraw, s: str, font, tracking: float = 0.0) -> int:
    if not s:
        return 0
    w = draw.textlength(s, font=font)
    if tracking:
        w += tracking * max(len(s) - 1, 0)
    return int(w)


def draw_tracked(draw, xy, s: str, font, fill, tracking: float) -> None:
    """Gambar teks dengan jarak antar huruf (letter-spacing)."""
    x, y = xy
    for ch in s:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking


def parse_spans(text: str) -> list[tuple[str, bool]]:
    """'A [B] C' -> [('A ', False), ('B', True), (' C', False)]"""
    spans: list[tuple[str, bool]] = []
    for part in re.split(r"(\[[^\]]*\])", text):
        if not part:
            continue
        if part.startswith("[") and part.endswith("]"):
            spans.append((part[1:-1], True))
        else:
            spans.append((part, False))
    return spans


# Satu kata bisa terdiri dari beberapa potongan warna, misalnya "[siap]."
# jadi [("siap", True), (".", False)] — tanpa spasi di antaranya.
Word = list[tuple[str, bool]]


def split_words(spans) -> list[Word]:
    """Pecah span jadi kata, tapi potongan yang nempel tetap satu kata."""
    words: list[Word] = []
    current: Word = []
    for text, hl in spans:
        for i, part in enumerate(text.split(" ")):
            if i > 0:  # ketemu spasi -> tutup kata sebelumnya
                if current:
                    words.append(current)
                current = []
            if part:
                current.append((part, hl))
    if current:
        words.append(current)
    return words


def word_text(word: Word) -> str:
    return "".join(t for t, _ in word)


def wrap_spans(draw, spans, font, max_w: int) -> list[list[Word]]:
    """Bungkus kata per baris sambil nyimpen info warna tiap potongan."""
    lines: list[list[Word]] = []
    current: list[Word] = []
    for word in split_words(spans):
        trial = current + [word]
        trial_w = text_width(draw, " ".join(word_text(w) for w in trial), font)
        if current and trial_w > max_w:
            lines.append(current)
            current = [word]
        else:
            current = trial
    if current:
        lines.append(current)
    return lines


def fit_headline(draw, spans, lo: Layout, max_lines: int = 4):
    """Kecilin ukuran font sampai headline muat dalam max_lines."""
    max_w = lo.w - lo.margin * 2
    size = lo.headline_size
    while size > int(52 * lo.s):
        font = load_font(FONT_HEADLINE, size)
        lines = wrap_spans(draw, spans, font, max_w)
        if len(lines) <= max_lines:
            return font, lines, size
        size -= 3
    font = load_font(FONT_HEADLINE, size)
    return font, wrap_spans(draw, spans, font, max_w), size


def paste_robot(canvas: Image.Image, spec: dict | None, lo: Layout) -> None:
    """Tempel maskot Para ke foto.

    Robotnya aset asli, bukan hasil generate — jadi bentuknya identik di semua
    slide. Ditempel sebelum gradasi biar ikut meleleh kayak bagian foto.

    spec: {"pose": "welcome", "x": 0.74, "y": 0.60, "scale": 0.30, "flip": false}
    x/y = titik kaki robot (rasio kanvas), scale = tinggi robot / tinggi area foto.
    """
    if not spec:
        return
    pose = spec.get("pose", "thinking")
    path = POSES / f"para-{pose}.png"
    if not path.exists():
        raise SystemExit(f"Pose Para nggak ketemu: {path}")

    src = Image.open(path).convert("RGBA")
    h = max(int(lo.panel_top * float(spec.get("scale", 0.30))), 1)
    w = max(int(src.width * h / src.height), 1)
    robot = src.resize((w, h), Image.LANCZOS)
    if spec.get("flip"):
        robot = robot.transpose(Image.FLIP_LEFT_RIGHT)

    feet_x = int(lo.w * float(spec.get("x", 0.74)))
    feet_y = int(lo.h * float(spec.get("y", 0.60)))
    x0, y0 = feet_x - w // 2, feet_y - h

    # Bayangan kontak biar robotnya napak, nggak ngambang.
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sw, sh = int(w * 0.62), max(int(h * 0.055), 3)
    sd.ellipse(
        [feet_x - sw // 2, feet_y - sh // 2, feet_x + sw // 2, feet_y + sh // 2],
        fill=(0, 0, 0, 105),
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(max(int(h * 0.035), 4)))
    canvas.paste(shadow, (0, 0), shadow)
    canvas.paste(robot, (x0, y0), robot)


def build_background(slide: dict, lo: Layout, demo: bool) -> Image.Image:
    canvas = Image.new("RGB", (lo.w, lo.h), PANEL)
    photo_path = slide.get("photo")

    if demo or not photo_path:
        # Placeholder: gradasi netral biar layout teksnya kelihatan.
        grad = Image.new("RGB", (1, lo.panel_top))
        gd = ImageDraw.Draw(grad)
        for y in range(grad.height):
            t = y / max(grad.height - 1, 1)
            gd.point((0, y), fill=(int(58 + 40 * t), int(64 + 44 * t), int(76 + 50 * t)))
        photo = grad.resize((lo.w, grad.height), Image.LANCZOS)
    else:
        p = Path(photo_path)
        if not p.exists():
            raise SystemExit(f"Foto nggak ketemu: {p}")
        src = Image.open(p).convert("RGB")
        target_h = lo.panel_top
        scale = max(lo.w / src.width, target_h / src.height)
        resized = src.resize(
            (max(int(src.width * scale), lo.w), max(int(src.height * scale), target_h)),
            Image.LANCZOS,
        )
        # crop_y: 0 = ambil bagian atas foto, 1 = bagian bawah. Foto potret
        # yang lebih tinggi dari area slide perlu digeser ke bawah biar meja
        # dan robotnya ikut kelihatan, bukan kepotong.
        left = (resized.width - lo.w) // 2
        top = int((resized.height - target_h) * float(slide.get("crop_y", 0.45)))
        photo = resized.crop((left, top, left + lo.w, top + target_h))

    canvas.paste(photo, (0, 0))
    paste_robot(canvas, slide.get("robot"), lo)

    # Lelehin bagian bawah foto ke panel biar nyambung, bukan garis potong.
    # Smootherstep (6t^5-15t^4+10t^3): kemiringannya nol di kedua ujung, jadi
    # nggak ada tepi yang kelihatan — baik di sisi foto maupun sisi panel.
    fade = Image.new("RGB", (lo.w, lo.fade), PANEL)
    mask = Image.new("L", (1, lo.fade))
    md = ImageDraw.Draw(mask)
    for y in range(lo.fade):
        t = y / max(lo.fade - 1, 1)
        md.point((0, y), fill=round(255 * (t * t * t * (t * (t * 6 - 15) + 10))))
    canvas.paste(fade, (0, lo.panel_top - lo.fade), mask.resize((lo.w, lo.fade)))
    canvas.paste(
        Image.new("RGB", (lo.w, lo.h - lo.panel_top), PANEL), (0, lo.panel_top)
    )
    return canvas


def render_slide(slide: dict, lo: Layout, demo: bool) -> Image.Image:
    canvas = build_background(slide, lo, demo)
    draw = ImageDraw.Draw(canvas)
    x = lo.margin
    y = lo.panel_top + int(66 * lo.s)

    kicker = slide.get("kicker", "").upper()
    if kicker:
        kf = load_font(FONT_BOLD, lo.kicker_size)
        draw_tracked(draw, (x, y), kicker, kf, NAVY, lo.kicker_track)
        y += lo.kicker_size + lo.gap_kicker

    spans = parse_spans(slide["headline"].upper())
    hf, lines, size = fit_headline(draw, spans, lo)
    line_h = int(size * lo.headline_lead)
    space_w = draw.textlength(" ", font=hf)
    for line in lines:
        cx = x
        for word in line:
            for part, hl in word:  # potongan nempel, tanpa spasi
                draw.text((cx, y), part, font=hf, fill=BLUE if hl else NAVY)
                cx += draw.textlength(part, font=hf)
            cx += space_w
        y += line_h

    sub = slide.get("sub")
    if sub:
        y += lo.gap_sub
        sf = load_font(FONT_SEMIBOLD, lo.sub_size)
        sw = draw.textlength(" ", font=sf)
        for line in wrap_spans(draw, parse_spans(sub), sf, lo.w - lo.margin * 2):
            cx = x
            for word in line:
                for part, hl in word:
                    draw.text((cx, y), part, font=sf, fill=BLUE if hl else INK_SOFT)
                    cx += draw.textlength(part, font=sf)
                cx += sw
            y += int(lo.sub_size * 1.34)

    handle = slide.get("handle")
    if handle:
        hfont = load_font(FONT_SEMIBOLD, lo.handle_size)
        draw.text((x, lo.h - lo.margin - lo.handle_size), handle, font=hfont, fill=(96, 108, 130))

    return canvas


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("spec", type=Path, help="file JSON berisi slide")
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument("--demo", action="store_true", help="pakai background placeholder")
    ap.add_argument("--size", default="1080x1920", help="misal 1080x1350 buat rasio 4:5")
    args = ap.parse_args()

    w, h = (int(v) for v in args.size.lower().split("x"))
    lo = Layout(w, h)
    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    slides = spec["slides"] if isinstance(spec, dict) else spec

    args.out.mkdir(parents=True, exist_ok=True)
    for i, slide in enumerate(slides, start=1):
        img = render_slide(slide, lo, args.demo)
        name = f"{i:02d}-{slide.get('slug', 'slide')}.png"
        img.save(args.out / name, "PNG", optimize=True)
        print(f"  {name}")
    print(f"\n{len(slides)} slide -> {args.out}")


if __name__ == "__main__":
    main()
