from pathlib import Path
from textwrap import shorten

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "Parameter-Instagram-DUIT-Content-Strategy.pdf"
LOGO = ROOT / "public" / "parameter-logo-white.png"

W, H = A4

INK = HexColor("#0E0F13")
SURFACE = HexColor("#1A1C22")
PANEL = HexColor("#23262D")
CREAM = HexColor("#F6F7F9")
MIST = HexColor("#9EA1A9")
SLATE = HexColor("#6A6D75")
BLUE = HexColor("#2D6BF5")
BLUE_BRIGHT = HexColor("#6FA0FF")
BLUE_SOFT = HexColor("#DCE7FF")
WHITE = HexColor("#FFFFFF")
GREEN = HexColor("#77D6A1")
YELLOW = HexColor("#FFD166")

MARGIN = 42


def wrap_text(text, font, size, max_width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = word if not current else current + " " + word
        if stringWidth(candidate, font, size) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(c, text, x, y, max_width, font="Helvetica", size=10.5,
                 color=CREAM, leading=None, max_lines=None):
    if leading is None:
        leading = size * 1.38
    lines = wrap_text(text, font, size, max_width)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = shorten(lines[-1], width=max(12, len(lines[-1]) - 2), placeholder="...")
    c.setFont(font, size)
    c.setFillColor(color)
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def rounded(c, x, y, w, h, fill=SURFACE, stroke=None, radius=14, width=1):
    c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke)
        c.setLineWidth(width)
        c.roundRect(x, y, w, h, radius, fill=1, stroke=1)
    else:
        c.roundRect(x, y, w, h, radius, fill=1, stroke=0)


def label(c, text, x, y, color=BLUE_BRIGHT):
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x, y, text.upper())


def page_base(c, page_no, section=None):
    c.setFillColor(INK)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setStrokeColor(HexColor("#2C2F36"))
    c.setLineWidth(0.7)
    c.line(MARGIN, 31, W - MARGIN, 31)
    c.setFont("Helvetica", 7.5)
    c.setFillColor(SLATE)
    c.drawString(MARGIN, 18, "PARAMETER / INSTAGRAM CONTENT SYSTEM / JULY 2026")
    c.drawRightString(W - MARGIN, 18, f"{page_no:02d}")
    if section:
        label(c, section, MARGIN, H - 38, MIST)


def title(c, text, y=H - 74, size=25, max_width=W - 2 * MARGIN):
    lines = wrap_text(text, "Helvetica-Bold", size, max_width)
    c.setFillColor(CREAM)
    c.setFont("Helvetica-Bold", size)
    for line in lines:
        c.drawString(MARGIN, y, line)
        y -= size * 1.12
    return y


def body(c, text, y, size=11, color=MIST, max_width=W - 2 * MARGIN):
    return draw_wrapped(c, text, MARGIN, y, max_width, size=size, color=color)


def bullet(c, text, x, y, width, accent=BLUE, size=9.5, color=CREAM):
    c.setFillColor(accent)
    c.circle(x + 3, y + 2.5, 2.8, fill=1, stroke=0)
    return draw_wrapped(c, text, x + 14, y + 6, width - 14, size=size,
                        color=color, leading=size * 1.42)


def stat_card(c, x, y, w, h, number, caption, source=None, accent=BLUE):
    rounded(c, x, y, w, h, PANEL, HexColor("#363A43"), 13)
    c.setFillColor(accent)
    c.setFont("Helvetica-Bold", 23)
    c.drawString(x + 15, y + h - 33, number)
    draw_wrapped(c, caption, x + 15, y + h - 53, w - 30, size=9.2,
                 color=CREAM, leading=12.5, max_lines=3)
    if source:
        c.setFont("Helvetica", 7)
        c.setFillColor(MIST)
        c.drawString(x + 15, y + 12, source)


def footer_source(c, text, url, y):
    c.setFillColor(MIST)
    c.setFont("Helvetica", 7.2)
    c.drawString(MARGIN, y, text)
    display = url.replace("https://", "")
    if len(display) > 76:
        display = display[:73] + "..."
    c.setFillColor(BLUE_BRIGHT)
    c.drawString(MARGIN, y - 11, display)
    c.linkURL(url, (MARGIN, y - 14, W - MARGIN, y + 2), relative=0)


def draw_cover(c):
    page_base(c, 1)
    c.setFillColor(BLUE)
    c.circle(W - 78, H - 77, 92, fill=1, stroke=0)
    c.setFillColor(HexColor("#1747B6"))
    c.circle(W - 40, H - 125, 58, fill=1, stroke=0)

    if LOGO.exists():
        img = ImageReader(str(LOGO))
        iw, ih = img.getSize()
        target_w = 132
        target_h = target_w * ih / iw
        c.drawImage(img, MARGIN, H - 73, target_w, target_h, mask="auto")
    else:
        c.setFont("Helvetica-Bold", 17)
        c.setFillColor(WHITE)
        c.drawString(MARGIN, H - 62, "PARAMETER")

    label(c, "CONTENT GROWTH PLAYBOOK", MARGIN, H - 160, BLUE_BRIGHT)
    c.setFillColor(CREAM)
    c.setFont("Helvetica-Bold", 36)
    c.drawString(MARGIN, H - 211, "D.U.I.T.")
    c.setFont("Helvetica-Bold", 29)
    c.drawString(MARGIN, H - 249, "Content Strategy")
    c.setFont("Helvetica-Bold", 29)
    c.drawString(MARGIN, H - 284, "for Instagram")

    c.setFillColor(MIST)
    c.setFont("Helvetica", 12)
    c.drawString(MARGIN, H - 324, "Emotion-first. Data-backed. No hard selling.")

    rounded(c, MARGIN, 98, W - 2 * MARGIN, 136, SURFACE, HexColor("#33363E"), 18)
    label(c, "NORTH STAR", MARGIN + 20, 207, GREEN)
    draw_wrapped(
        c,
        "Membantu orang yang punya skill, ide, atau usaha mengubahnya menjadi penghasilan digital - tanpa harus jalan sendirian.",
        MARGIN + 20, 181, W - 2 * MARGIN - 40,
        font="Helvetica-Bold", size=15, color=CREAM, leading=20,
    )
    c.setFillColor(MIST)
    c.setFont("Helvetica", 8.5)
    c.drawString(MARGIN + 20, 116, "Prepared for @parameter.id2026 / July 2026")
    c.showPage()


def draw_positioning(c):
    page_base(c, 2, "01 / POSITIONING")
    y = title(c, "Jangan jual website. Jual rasa tidak sendirian.")
    y -= 12
    y = body(c, "Parameter bukan sekadar vendor teknologi. Parameter adalah partner yang menemani audiens dari kebingungan pertama sampai bisnis digitalnya punya arah, alat, dan jalur pertumbuhan.", y)

    stages = [
        ("01", "Diskusi", "Memetakan skill, ide, masalah, dan target pendapatan."),
        ("02", "Validasi", "Menguji siapa yang membutuhkan dan mau membayar."),
        ("03", "Bangun", "Membuat bisnis, produk, website, aplikasi, atau tools yang tepat."),
        ("04", "Tumbuh", "Merapikan akuisisi, operasional, data, dan repeat order."),
        ("05", "Belajar", "Meningkatkan kemampuan lewat edukasi dan ekosistem Lamuri."),
    ]
    top = 542
    for i, (num, head, desc) in enumerate(stages):
        yy = top - i * 82
        rounded(c, MARGIN, yy, W - 2 * MARGIN, 64, SURFACE, HexColor("#343840"), 12)
        c.setFillColor(BLUE)
        c.setFont("Helvetica-Bold", 15)
        c.drawString(MARGIN + 16, yy + 35, num)
        c.setFillColor(CREAM)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(MARGIN + 58, yy + 38, head)
        draw_wrapped(c, desc, MARGIN + 58, yy + 22, W - 2 * MARGIN - 76,
                     size=8.8, color=MIST, leading=11)

    rounded(c, MARGIN, 82, W - 2 * MARGIN, 72, HexColor("#142858"), BLUE, 13)
    label(c, "CORE MESSAGE", MARGIN + 17, 131, BLUE_BRIGHT)
    draw_wrapped(c, "Dari 'gue mulai dari mana?' sampai 'bisnis gue sudah jalan.'",
                 MARGIN + 17, 109, W - 2 * MARGIN - 34,
                 font="Helvetica-Bold", size=13, color=WHITE)
    c.showPage()


def draw_audience(c):
    page_base(c, 3, "02 / AUDIENCE")
    y = title(c, "Emosinya universal. Audiensnya tetap spesifik.")
    y -= 10
    body(c, "Target utama: orang yang punya skill, ide, atau usaha, tetapi belum tahu cara mengubahnya menjadi penghasilan digital yang rapi.", y)

    cards = [
        ("Punya skill", "Bisa desain, mengajar, memasak, konsultasi, atau membuat sesuatu - tetapi belum tahu cara menjualnya."),
        ("Punya ide", "Melihat peluang, tetapi takut salah langkah, rugi, atau membangun produk yang tidak dibutuhkan."),
        ("Punya usaha", "Sudah punya customer, tetapi penjualan stagnan dan semuanya masih bergantung pada owner."),
        ("Butuh teman jalan", "Sudah menonton banyak tutorial, tetapi tetap bingung menentukan langkah pertama yang paling relevan."),
    ]
    positions = [(MARGIN, 422), (W/2 + 6, 422), (MARGIN, 258), (W/2 + 6, 258)]
    cw = (W - 2 * MARGIN - 12) / 2
    for (head, desc), (x, yy) in zip(cards, positions):
        rounded(c, x, yy, cw, 140, SURFACE, HexColor("#343840"), 15)
        c.setFillColor(BLUE)
        c.rect(x + 15, yy + 108, 26, 4, fill=1, stroke=0)
        c.setFillColor(CREAM)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(x + 15, yy + 84, head)
        draw_wrapped(c, desc, x + 15, yy + 62, cw - 30, size=9, color=MIST, leading=12)

    rounded(c, MARGIN, 87, W - 2 * MARGIN, 116, PANEL, HexColor("#3C4049"), 15)
    label(c, "EMOTIONAL PROMISE", MARGIN + 18, 177, YELLOW)
    draw_wrapped(c, "Lo tidak harus punya semua jawabannya hari ini. Mulai dari cerita, lalu kita petakan jalannya bareng.",
                 MARGIN + 18, 148, W - 2 * MARGIN - 36,
                 font="Helvetica-Bold", size=14, color=CREAM, leading=19)
    c.showPage()


def draw_framework(c):
    page_base(c, 4, "03 / FRAMEWORK")
    y = title(c, "D.U.I.T. - alur emosi setiap Reel")
    y -= 12
    body(c, "Gunakan pola ini untuk memindahkan audiens dari rasa cemas menuju rasa mampu dan ditemani.", y)

    items = [
        ("D", "Data nyata", "Buka dengan angka aktual dan sumber yang jelas.", BLUE),
        ("U", "Ungkap keresahan", "Terjemahkan angka menjadi situasi yang mereka rasakan.", YELLOW),
        ("I", "Insight dan jalan", "Berikan 1-3 langkah realistis, bukan motivasi kosong.", GREEN),
        ("T", "Temani", "Undang follow dan chat tanpa memaksa membeli.", BLUE_BRIGHT),
    ]
    top = 535
    for i, (letter, head, desc, accent) in enumerate(items):
        yy = top - i * 103
        rounded(c, MARGIN, yy, W - 2 * MARGIN, 82, SURFACE, HexColor("#353941"), 14)
        c.setFillColor(accent)
        c.circle(MARGIN + 34, yy + 41, 21, fill=1, stroke=0)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(MARGIN + 34, yy + 35, letter)
        c.setFillColor(CREAM)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(MARGIN + 72, yy + 50, head)
        draw_wrapped(c, desc, MARGIN + 72, yy + 29, W - 2 * MARGIN - 92,
                     size=9.2, color=MIST, leading=12)

    rounded(c, MARGIN, 79, W - 2 * MARGIN, 75, HexColor("#142858"), BLUE, 14)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 11.5)
    c.drawString(MARGIN + 17, 126, "Cemas -> Dipahami -> Melihat peluang -> Merasa mampu -> Mau berdiskusi")
    draw_wrapped(c, "Jangan gunakan: takut -> dipermalukan -> disuruh membeli.",
                 MARGIN + 17, 104, W - 2 * MARGIN - 34, size=9, color=BLUE_SOFT)
    c.showPage()


def draw_hooks(c):
    page_base(c, 5, "04 / FIRST 3 SECONDS")
    y = title(c, "Angka + kontras emosional + open loop")
    y -= 10
    body(c, "Scene pertama harus bisa dibaca sebelum audiens sempat scroll. Maksimal 8-12 kata, satu angka besar, dan satu konflik yang belum selesai.", y)

    hooks = [
        ("Rp3,29 juta", "Kalau angka ini terasa tidak cukup, lo tidak sendirian."),
        ("7,24 juta", "orang masih mencari kerja. Tapi peluang digital terus tumbuh."),
        ("231 juta", "orang Indonesia sudah online. Apakah mereka bisa menemukan bisnis lo?"),
        ("64 juta UMKM", "baru sekitar 40% yang masuk ekosistem digital."),
        ("US$105 miliar", "nilai pasar digital Indonesia. Banyak orang tetap bingung mulai."),
        ("97% tenaga kerja", "ditopang UMKM. Banyak owner masih bekerja sendirian."),
    ]
    yy = 521
    for number, rest in hooks:
        rounded(c, MARGIN, yy, W - 2 * MARGIN, 65, SURFACE, HexColor("#343840"), 12)
        c.setFillColor(BLUE_BRIGHT)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(MARGIN + 15, yy + 37, number)
        draw_wrapped(c, rest, MARGIN + 138, yy + 38, W - MARGIN - (MARGIN + 154),
                     font="Helvetica-Bold", size=9.4, color=CREAM, leading=12)
        yy -= 76

    rounded(c, MARGIN, 72, W - 2 * MARGIN, 56, PANEL, None, 12)
    label(c, "RULE", MARGIN + 15, 107, GREEN)
    draw_wrapped(c, "Jangan selesaikan masalah di scene pertama. Buat audiens merasa: ini gue - lalu beri alasan untuk lanjut.",
                 MARGIN + 15, 88, W - 2 * MARGIN - 30, size=8.8, color=CREAM)
    c.showPage()


def draw_data_bank(c):
    page_base(c, 6, "05 / DATA BANK")
    y = title(c, "Angka yang bisa langsung jadi hook")
    y -= 9
    body(c, "Gunakan angka sebagai pintu masuk, lalu beri konteks yang akurat. Jangan mengubah korelasi menjadi janji penghasilan.", y)

    cw = (W - 2 * MARGIN - 12) / 2
    stat_card(c, MARGIN, 468, cw, 118, "Rp3,29 juta", "Rata-rata upah buruh Indonesia pada Februari 2026.", "BPS, May 2026", BLUE)
    stat_card(c, W/2 + 6, 468, cw, 118, "7,24 juta", "Penduduk masih menganggur pada Februari 2026.", "BPS, May 2026", YELLOW)
    stat_card(c, MARGIN, 332, cw, 118, "87,74 juta", "Penduduk bekerja dalam kegiatan informal.", "BPS, May 2026", GREEN)
    stat_card(c, W/2 + 6, 332, cw, 118, "231 juta", "Penduduk Indonesia terhubung ke internet.", "Komdigi, Apr 2026", BLUE_BRIGHT)
    stat_card(c, MARGIN, 196, cw, 118, "64 juta", "Jumlah UMKM; baru sekitar 40% masuk ekosistem digital.", "Komdigi, Apr 2026", BLUE)
    stat_card(c, W/2 + 6, 196, cw, 118, "US$105B", "Perkiraan nilai ekonomi digital Indonesia pada 2025.", "Komdigi, Jun 2026", YELLOW)

    footer_source(c, "BPS - Keadaan Ketenagakerjaan Februari 2026", "https://www.bps.go.id/id/pressrelease/2026/05/05/2574/", 157)
    footer_source(c, "Komdigi - UMKM, internet, dan meaningful connectivity", "https://portal.komdigi.go.id/kanal-publik/berita-kini/10176", 125)
    footer_source(c, "Komdigi - Proyeksi ekonomi digital Indonesia", "https://portal.komdigi.go.id/kanal-publik/berita-kini/10338", 93)
    c.showPage()


def draw_pillars(c):
    page_base(c, 7, "06 / CONTENT PILLARS")
    y = title(c, "Konten memberi harapan sekaligus pegangan")
    y -= 10
    body(c, "Parameter tidak menjual mimpi kaya cepat. Parameter menunjukkan bahwa peluang digital itu nyata, lalu membantu audiens mengambil langkah yang masuk akal.", y)

    pillars = [
        ("35%", "Realita Duit Hari Ini", "Upah, pekerjaan, UMKM, pasar digital, dan tekanan yang benar-benar terjadi.", BLUE),
        ("25%", "Mulai Menghasilkan", "Validasi skill, memilih masalah, menemukan pembeli, dan mendapat customer pertama.", GREEN),
        ("20%", "Bangun Sistemnya", "Landing page, order flow, CRM, automasi, dashboard, pembayaran, dan tools.", YELLOW),
        ("10%", "Belajar di Lamuri", "Mini lesson, roadmap skill, framework bisnis, dan cuplikan proses belajar.", BLUE_BRIGHT),
        ("10%", "Ditemani Parameter", "Diskusi awal, proses kerja, case, keputusan, dan pendampingan setelah launch.", CREAM),
    ]
    yy = 527
    for pct, head, desc, accent in pillars:
        rounded(c, MARGIN, yy, W - 2 * MARGIN, 72, SURFACE, HexColor("#353941"), 13)
        c.setFillColor(accent)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(MARGIN + 15, yy + 40, pct)
        c.setFillColor(CREAM)
        c.setFont("Helvetica-Bold", 11.5)
        c.drawString(MARGIN + 76, yy + 44, head)
        draw_wrapped(c, desc, MARGIN + 76, yy + 26, W - 2 * MARGIN - 96,
                     size=8.4, color=MIST, leading=11)
        yy -= 84

    rounded(c, MARGIN, 76, W - 2 * MARGIN, 55, HexColor("#142858"), BLUE, 12)
    draw_wrapped(c, "Satu dari sepuluh konten boleh bicara layanan. Sembilan lainnya harus membuat audiens merasa lebih paham, lebih siap, atau lebih ditemani.",
                 MARGIN + 16, 108, W - 2 * MARGIN - 32,
                 font="Helvetica-Bold", size=9.2, color=WHITE, leading=12)
    c.showPage()


def draw_reel_template(c):
    page_base(c, 8, "07 / REEL TEMPLATE")
    y = title(c, "Carousel yang bergerak, bukan slide yang dipindah")
    y -= 10
    body(c, "Format 9:16, 20-35 detik, 8-9 scene. Visual bersih, teks singkat, ritme cepat, dan satu pesan utama.", y)

    scenes = [
        ("00-02s", "Hook", "Angka besar + konflik emosional."),
        ("02-05s", "Relate", "Tunjukkan kenyataan yang audiens alami."),
        ("05-09s", "Tension", "Jelaskan kenapa masalahnya tidak sesederhana kelihatannya."),
        ("09-20s", "Insight", "Berikan 1-3 parameter atau langkah."),
        ("20-27s", "Example", "Simulasi, perhitungan, atau contoh keadaan."),
        ("27-35s", "CTA", "Follow untuk lanjut. Chat untuk diskusi."),
    ]
    yy = 526
    for time, head, desc in scenes:
        c.setFillColor(BLUE)
        c.roundRect(MARGIN, yy + 4, 62, 27, 7, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawCentredString(MARGIN + 31, yy + 14, time)
        c.setFillColor(CREAM)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(MARGIN + 79, yy + 22, head)
        draw_wrapped(c, desc, MARGIN + 150, yy + 23, W - MARGIN - (MARGIN + 150),
                     size=8.7, color=MIST, leading=11)
        c.setStrokeColor(HexColor("#31343B"))
        c.line(MARGIN, yy - 8, W - MARGIN, yy - 8)
        yy -= 66

    rounded(c, MARGIN, 83, W - 2 * MARGIN, 86, SURFACE, HexColor("#353941"), 13)
    label(c, "MOTION RULES", MARGIN + 16, 143, GREEN)
    rules = "Scene berganti setiap 1,5-3 detik / progress bar / zoom 2-4% / highlight angka / SFX kecil / musik hanya pendukung / maksimal 8-12 kata per scene."
    draw_wrapped(c, rules, MARGIN + 16, 120, W - 2 * MARGIN - 32,
                 size=9.3, color=CREAM, leading=13)
    c.showPage()


def draw_script_page(c, page_no, label_text, headline, scenes, source_text):
    page_base(c, page_no, "08 / READY-TO-PRODUCE SCRIPTS")
    label(c, label_text, MARGIN, H - 70, BLUE_BRIGHT)
    y = title(c, headline, y=H - 104, size=24)
    y -= 7
    for i, (scene, copy) in enumerate(scenes, start=1):
        h = 52 if len(copy) < 85 else 65
        rounded(c, MARGIN, y - h + 8, W - 2 * MARGIN, h, SURFACE, HexColor("#343840"), 12)
        c.setFillColor(BLUE)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(MARGIN + 13, y - 11, f"S{i:02d} / {scene}")
        draw_wrapped(c, copy, MARGIN + 88, y - 7, W - 2 * MARGIN - 103,
                     font="Helvetica-Bold" if i == 1 else "Helvetica",
                     size=10.2 if i == 1 else 9.2,
                     color=CREAM, leading=13)
        y -= h + 10
    rounded(c, MARGIN, 66, W - 2 * MARGIN, 55, HexColor("#142858"), BLUE, 12)
    label(c, "CTA", MARGIN + 14, 99, GREEN)
    draw_wrapped(c, "Follow @parameter.id2026 buat lanjut belajar. Kalau lo mau diskusi soal ide atau usaha lo, chat 'MULAI'.",
                 MARGIN + 14, 81, W - 2 * MARGIN - 28,
                 font="Helvetica-Bold", size=8.7, color=WHITE, leading=11)
    c.setFont("Helvetica", 6.8)
    c.setFillColor(MIST)
    c.drawRightString(W - MARGIN, 130, source_text)
    c.showPage()


def draw_cta_library(c):
    page_base(c, 12, "09 / CTA LIBRARY")
    y = title(c, "Follow untuk belajar. Chat untuk mulai bicara.")
    y -= 8
    body(c, "CTA harus terasa seperti pintu masuk percakapan, bukan tombol checkout. Gunakan satu versi per Reel agar pesannya jelas.", y)

    ctas = [
        ("EDUKASI", "Follow @parameter.id2026. Kita lanjut bongkar langkah berikutnya besok."),
        ("EMOSI", "Follow biar lo tidak perlu mencari jalannya sendirian."),
        ("DISKUSI", "Punya ide tapi bingung mulai? Chat 'MULAI'. Kita petakan dulu."),
        ("UMKM", "Kalau bisnis lo ramai tapi masih berantakan, ceritain lewat chat. Kita diskusi dulu."),
        ("SKILL", "Punya skill tapi belum tahu cara menjualnya? Follow, lalu chat 'SKILL'."),
        ("SOFT", "Tidak harus langsung bikin apa-apa. Kalau mau ngobrol soal arahnya, chat aja."),
    ]
    yy = 516
    for tag, copy in ctas:
        rounded(c, MARGIN, yy, W - 2 * MARGIN, 64, SURFACE, HexColor("#353941"), 12)
        label(c, tag, MARGIN + 14, yy + 39, BLUE_BRIGHT)
        draw_wrapped(c, copy, MARGIN + 94, yy + 40, W - 2 * MARGIN - 110,
                     font="Helvetica-Bold", size=9.4, color=CREAM, leading=12)
        yy -= 75

    rounded(c, MARGIN, 74, W - 2 * MARGIN, 72, PANEL, HexColor("#3A3E47"), 12)
    label(c, "DEFAULT CTA", MARGIN + 15, 121, GREEN)
    draw_wrapped(c, "Follow @parameter.id2026 buat belajar membangun penghasilan digital. Kalau lo mau diskusi soal kondisi lo, chat aja - mulai dari cerita dulu.",
                 MARGIN + 15, 100, W - 2 * MARGIN - 30,
                 font="Helvetica-Bold", size=9.5, color=WHITE, leading=13)
    c.showPage()


def draw_calendar(c):
    page_base(c, 13, "10 / 30-DAY SPRINT")
    y = title(c, "24 Reels untuk menemukan tema pemenang")
    y -= 7
    body(c, "Posting 6 Reel per minggu. Minggu dipakai untuk membaca insight, menulis batch baru, dan menggandakan tema yang paling banyak menghasilkan share, save, profile visit, follow, dan chat.", y, size=9.7)

    weeks = [
        ("W1 / REALITA", [
            "Rp3,29 juta: kenapa banyak orang mencari penghasilan tambahan",
            "7,24 juta orang masih cari kerja - mulai digital dari mana?",
            "Punya skill tetapi belum tahu siapa yang mau membayar",
            "Kerja keras tidak otomatis menjadi sistem penghasilan",
            "Bedanya side hustle, jasa, dan produk digital",
            "Lo tidak malas. Mungkin lo cuma tidak punya arah",
        ]),
        ("W2 / PELUANG", [
            "US$105B: pasarnya besar, jalur masuknya harus jelas",
            "231 juta orang online - siapa yang bisa lo bantu?",
            "Cara memilih masalah yang layak dibayar",
            "Customer pertama tidak dimulai dari logo",
            "Tiga bisnis digital yang bisa dimulai dari skill",
            "Validasi ide tanpa langsung bikin aplikasi",
        ]),
        ("W3 / SISTEM", [
            "64 juta UMKM, baru 40% masuk ekosistem digital",
            "Punya Instagram bukan berarti punya jalur penjualan",
            "Tiga tanda bisnis sudah butuh landing page",
            "Kenapa order hilang di tumpukan chat",
            "Tools sederhana untuk menyimpan data customer",
            "Go online vs go produktif",
        ]),
        ("W4 / DITEMANI", [
            "Apa yang kami tanyakan sebelum menyarankan tools",
            "Kenapa kami sering bilang: jangan bikin aplikasi dulu",
            "Dari ide mentah ke produk pertama",
            "Setelah launch, pekerjaan sebenarnya baru dimulai",
            "Belajar skill digital lewat Lamuri",
            "Punya ide? Mulai dari cerita, bukan proposal",
        ]),
    ]

    yy = 523
    for week, ideas in weeks:
        rounded(c, MARGIN, yy - 116, W - 2 * MARGIN, 125, SURFACE, HexColor("#353941"), 13)
        label(c, week, MARGIN + 14, yy - 14, BLUE_BRIGHT)
        col_w = (W - 2 * MARGIN - 42) / 2
        for idx, idea in enumerate(ideas):
            col = idx // 3
            row = idx % 3
            x = MARGIN + 14 + col * (col_w + 14)
            iy = yy - 39 - row * 27
            c.setFillColor(BLUE)
            c.circle(x + 3, iy + 2, 2.4, fill=1, stroke=0)
            draw_wrapped(c, idea, x + 12, iy + 5, col_w - 12,
                         size=7.6, color=CREAM, leading=9.5, max_lines=2)
        yy -= 139

    rounded(c, MARGIN, 60, W - 2 * MARGIN, 44, HexColor("#142858"), BLUE, 11)
    draw_wrapped(c, "Setiap Reel wajib punya satu CTA: follow untuk seri berikutnya atau chat untuk diskusi. Tidak perlu keduanya ditulis panjang.",
                 MARGIN + 13, 86, W - 2 * MARGIN - 26,
                 font="Helvetica-Bold", size=8.2, color=WHITE, leading=10)
    c.showPage()


def draw_metrics(c):
    page_base(c, 14, "11 / MEASUREMENT")
    y = title(c, "Optimasi untuk percakapan, bukan vanity")
    y -= 9
    body(c, "Pertumbuhan follower adalah hasil. Sistem konten harus mengukur apakah orang berhenti, memahami, percaya, lalu memulai percakapan.", y)

    metrics = [
        ("STOP", "Average watch time dan retensi awal", "Apakah hook tiga detik bekerja?"),
        ("VALUE", "Share dan save per reach", "Apakah konten cukup berguna atau relatable?"),
        ("TRUST", "Profile visit per reach", "Apakah audiens ingin mengenal Parameter?"),
        ("GROWTH", "Follow per profile visit", "Apakah positioning akun sudah jelas?"),
        ("INTENT", "Chat berkualitas per Reel", "Apakah konten membuka percakapan yang relevan?"),
    ]
    yy = 520
    for tag, metric, question in metrics:
        rounded(c, MARGIN, yy, W - 2 * MARGIN, 72, SURFACE, HexColor("#353941"), 13)
        label(c, tag, MARGIN + 15, yy + 45, GREEN)
        c.setFillColor(CREAM)
        c.setFont("Helvetica-Bold", 10.5)
        c.drawString(MARGIN + 90, yy + 45, metric)
        draw_wrapped(c, question, MARGIN + 90, yy + 25, W - 2 * MARGIN - 105,
                     size=8.7, color=MIST, leading=11)
        yy -= 84

    rounded(c, MARGIN, 82, W - 2 * MARGIN, 81, PANEL, HexColor("#3A3E47"), 13)
    label(c, "WINNER RULE", MARGIN + 16, 137, YELLOW)
    draw_wrapped(c, "Setiap 10 Reel, bandingkan dengan median akun. Jika share, follow, atau chat per reach minimal 1,5x median, buat 3-5 variasi dari tema yang sama.",
                 MARGIN + 16, 114, W - 2 * MARGIN - 32,
                 font="Helvetica-Bold", size=9.4, color=CREAM, leading=13)
    c.showPage()


def draw_sources(c):
    page_base(c, 15, "12 / SOURCES")
    y = title(c, "Riset dan aturan penggunaan data")
    y -= 10
    body(c, "Gunakan tanggal dan konteks sumber dalam caption. Hindari menjanjikan penghasilan, menakut-nakuti audiens, atau menyimpulkan bahwa semua pekerja informal mengalami kondisi yang sama.", y)

    sources = [
        ("BPS - Ketenagakerjaan Februari 2026", "Upah rata-rata Rp3,29 juta; TPT 4,68%; 154,91 juta angkatan kerja; 147,67 juta penduduk bekerja.", "https://www.bps.go.id/id/pressrelease/2026/05/05/2574/"),
        ("BPS - Ekonomi dan pekerja informal", "7,24 juta penganggur dan 87,74 juta pekerja informal pada Februari 2026.", "https://www.bps.go.id/en/news/2026/05/06/910/"),
        ("Komdigi - Creative-tech fusion", "64 juta UMKM; sekitar 40% masuk ekosistem digital; lebih dari 80% populasi atau sekitar 231 juta penduduk menggunakan internet.", "https://portal.komdigi.go.id/kanal-publik/berita-kini/10176"),
        ("Komdigi - Ekonomi digital", "Ekonomi digital Indonesia diperkirakan US$105 miliar pada 2025 dan berpotensi mencapai US$260-360 miliar.", "https://portal.komdigi.go.id/kanal-publik/berita-kini/10338"),
        ("Komdigi - Peran UMKM", "64,2 juta UMKM menyumbang sekitar 61% PDB dan menopang hampir 97% tenaga kerja.", "https://portal.komdigi.go.id/kanal-publik/berita-kini/10001"),
        ("Komdigi - Go productive", "Ukuran digitalisasi bukan sekadar online, tetapi kapasitas, perluasan pasar, produktivitas, dan daya saing.", "https://portal.komdigi.go.id/kanal-publik/berita-kini/10139"),
    ]
    col_gap = 12
    card_w = (W - 2 * MARGIN - col_gap) / 2
    card_h = 137
    top_y = 424
    for idx, (head, desc, url) in enumerate(sources):
        col = idx % 2
        row = idx // 2
        x = MARGIN + col * (card_w + col_gap)
        yy = top_y - row * 149
        rounded(c, x, yy, card_w, card_h, SURFACE, HexColor("#353941"), 12)
        draw_wrapped(c, head, x + 14, yy + card_h - 24, card_w - 28,
                     font="Helvetica-Bold", size=9.2, color=CREAM, leading=11, max_lines=2)
        draw_wrapped(c, desc, x + 14, yy + card_h - 53, card_w - 28,
                     size=7.7, color=MIST, leading=10, max_lines=4)
        display = url.replace("https://", "")
        if len(display) > 45:
            display = display[:42] + "..."
        c.setFillColor(BLUE_BRIGHT)
        c.setFont("Helvetica", 6.5)
        c.drawString(x + 14, yy + 15, display)
        c.linkURL(url, (x + 14, yy + 11, x + card_w - 14, yy + 25), relative=0)

    rounded(c, MARGIN, 57, W - 2 * MARGIN, 45, BLUE, None, 12)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 9.5)
    c.drawCentredString(W / 2, 76, "FOLLOW UNTUK BELAJAR. CHAT UNTUK DISKUSI. MULAI DARI CERITA.")
    c.showPage()


def build_pdf():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUTPUT), pagesize=A4)
    c.setTitle("Parameter Instagram D.U.I.T. Content Strategy")
    c.setAuthor("Parameter")
    c.setSubject("Emotion-first, data-backed Instagram content strategy")

    draw_cover(c)
    draw_positioning(c)
    draw_audience(c)
    draw_framework(c)
    draw_hooks(c)
    draw_data_bank(c)
    draw_pillars(c)
    draw_reel_template(c)

    draw_script_page(c, 9, "SCRIPT 01 / REALITA UPAH", "Rp3,29 juta terasa tidak cukup?", [
        ("HOOK", "Rp3,29 juta per bulan."),
        ("DATA", "Itu rata-rata upah buruh Indonesia pada Februari 2026."),
        ("RELATE", "Kalau angka itu terasa sempit buat hidup lo, perasaan lo valid."),
        ("TENSION", "Wajar kalau lo mulai bertanya: gue bisa dapat penghasilan tambahan dari mana?"),
        ("INSIGHT", "Jangan mulai dari produk. Mulai dari skill yang lo punya, masalah yang bisa lo selesaikan, dan siapa yang mau membayar."),
        ("CLOSE", "Skill + masalah nyata + pembeli adalah awal bisnis digital."),
    ], "Source: BPS, May 2026")

    draw_script_page(c, 10, "SCRIPT 02 / DIGITAL MARKET", "231 juta orang sudah online", [
        ("HOOK", "231 juta orang Indonesia sudah online."),
        ("OPEN LOOP", "Masalahnya, mereka belum tentu menemukan bisnis lo."),
        ("REFRAME", "Punya Instagram bukan berarti punya audiens. Punya website bukan berarti punya penjualan."),
        ("INSIGHT", "Lo butuh tiga jalur: konten untuk ditemukan, halaman untuk dipercaya, dan sistem untuk membeli."),
        ("CLOSE", "Teknologinya bukan tujuan. Tujuannya adalah membuat orang lebih mudah mengenal, percaya, dan membeli."),
    ], "Source: Komdigi, April 2026")

    draw_script_page(c, 11, "SCRIPT 03 / UMKM", "64 juta UMKM. Baru 40% masuk digital.", [
        ("HOOK", "Ada sekitar 64 juta UMKM. Baru sekitar 40% masuk ekosistem digital."),
        ("REFRAME", "Go online bukan sekadar membuat akun dan mengunggah foto produk."),
        ("TENSION", "Banyak bisnis masih kehilangan order, data pelanggan, repeat order, dan waktu owner."),
        ("INSIGHT", "Go produktif berarti punya alur penjualan, operasional, data, dan follow-up yang bisa diulang."),
        ("CLOSE", "Bisnis tidak selalu butuh aplikasi besar. Bisnis butuh sistem yang tepat untuk masalahnya."),
    ], "Source: Komdigi, April 2026")

    draw_cta_library(c)
    draw_calendar(c)
    draw_metrics(c)
    draw_sources(c)
    c.save()
    print(OUTPUT)


if __name__ == "__main__":
    build_pdf()
