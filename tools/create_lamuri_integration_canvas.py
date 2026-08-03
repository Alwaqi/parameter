from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "Lamuri-PlatformBelajar-Architecture-Mindmap.pdf"

PAGE_W, PAGE_H = landscape(A3)

INK = colors.HexColor("#14213D")
MUTED = colors.HexColor("#5F6B7A")
PAPER = colors.HexColor("#F7F4EE")
WHITE = colors.HexColor("#FFFFFF")
LINE = colors.HexColor("#D9DEE7")
NAVY = colors.HexColor("#14213D")
BLUE = colors.HexColor("#3157D5")
BLUE_TINT = colors.HexColor("#EAF0FF")
TEAL = colors.HexColor("#008B7A")
TEAL_TINT = colors.HexColor("#E5F7F2")
CORAL = colors.HexColor("#F06449")
CORAL_TINT = colors.HexColor("#FFF0EB")
AMBER = colors.HexColor("#E8A020")
AMBER_TINT = colors.HexColor("#FFF5DB")
PURPLE = colors.HexColor("#6D4AFF")
PURPLE_TINT = colors.HexColor("#F0ECFF")
GREEN = colors.HexColor("#1E8E5A")
GREEN_TINT = colors.HexColor("#E7F7EF")


def register_fonts():
    regular = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
    bold = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")
    if regular.exists() and bold.exists():
        pdfmetrics.registerFont(TTFont("CanvasRegular", str(regular)))
        pdfmetrics.registerFont(TTFont("CanvasBold", str(bold)))
        return "CanvasRegular", "CanvasBold"
    return "Helvetica", "Helvetica-Bold"


FONT, FONT_BOLD = register_fonts()


def style(size, color=INK, bold=False, leading=None, align=TA_LEFT):
    return ParagraphStyle(
        name=f"s-{size}-{bold}-{color}",
        fontName=FONT_BOLD if bold else FONT,
        fontSize=size,
        leading=leading or size * 1.25,
        textColor=color,
        alignment=align,
        spaceAfter=0,
        spaceBefore=0,
    )


def paragraph(c, text, x, y, w, h, size=8, color=INK, bold=False, leading=None):
    p = Paragraph(text, style(size, color, bold, leading))
    pw, ph = p.wrap(w, h)
    p.drawOn(c, x, y + h - ph)
    return ph


def rounded_box(c, x, y, w, h, fill, stroke=LINE, radius=10, stroke_width=0.8):
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.setLineWidth(stroke_width)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1)


def pill(c, text, x, y, w, fill, color, border=None):
    rounded_box(c, x, y, w, 18, fill, border or fill, radius=9, stroke_width=0.6)
    c.setFont(FONT_BOLD, 7.2)
    c.setFillColor(color)
    c.drawCentredString(x + w / 2, y + 5.2, text)


def arrow(c, x1, y1, x2, y2, color=LINE, width=1.6):
    c.setStrokeColor(color)
    c.setFillColor(color)
    c.setLineWidth(width)
    c.line(x1, y1, x2 - 6, y2)
    c.saveState()
    c.translate(x2, y2)
    c.rotate(0 if x2 >= x1 else 180)
    path = c.beginPath()
    path.moveTo(0, 0)
    path.lineTo(-7, 4)
    path.lineTo(-7, -4)
    path.close()
    c.drawPath(path, fill=1, stroke=0)
    c.restoreState()


def flow_card(c, x, y, w, h, number, title, body, accent, tint, meta=None):
    rounded_box(c, x, y, w, h, WHITE, LINE, radius=9)
    c.setFillColor(accent)
    c.circle(x + 15, y + h - 15, 8, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont(FONT_BOLD, 7)
    c.drawCentredString(x + 15, y + h - 17.7, str(number))
    paragraph(c, title, x + 28, y + h - 27, w - 36, 18, 8.2, INK, True, 9.2)
    paragraph(c, body, x + 12, y + 20, w - 24, h - 52, 6.8, MUTED, False, 8.4)
    if meta:
        c.setFillColor(tint)
        c.roundRect(x + 10, y + 7, w - 20, 13, 6.5, fill=1, stroke=0)
        c.setFont(FONT_BOLD, 5.9)
        c.setFillColor(accent)
        c.drawCentredString(x + w / 2, y + 10.8, meta)


def lane_label(c, x, y, w, h, title, subtitle, accent, tint):
    rounded_box(c, x, y, w, h, tint, tint, radius=10)
    c.setFillColor(accent)
    c.rect(x, y, 5, h, fill=1, stroke=0)
    paragraph(c, title, x + 16, y + h - 34, w - 25, 18, 9, accent, True, 10)
    paragraph(c, subtitle, x + 16, y + 12, w - 25, h - 48, 6.6, MUTED, False, 8)


def section_card(c, x, y, w, h, eyebrow, title, accent, tint):
    rounded_box(c, x, y, w, h, WHITE, LINE, radius=12)
    c.setFillColor(tint)
    c.roundRect(x + 12, y + h - 28, 76, 16, 8, fill=1, stroke=0)
    c.setFont(FONT_BOLD, 6.4)
    c.setFillColor(accent)
    c.drawString(x + 20, y + h - 22.7, eyebrow.upper())
    paragraph(c, title, x + 12, y + h - 52, w - 24, 21, 10.2, INK, True, 11.4)


def bullet(c, text, x, y, w, color=INK, accent=BLUE, size=6.8, leading=8.7):
    c.setFillColor(accent)
    c.circle(x + 3, y + 4.5, 2.1, fill=1, stroke=0)
    paragraph(c, text, x + 11, y, w - 11, leading * 2.3, size, color, False, leading)


def curved_connector(c, x1, y1, x2, y2, color, width=2.2):
    c.setStrokeColor(color)
    c.setLineWidth(width)
    mid_x = (x1 + x2) / 2
    c.bezier(x1, y1, mid_x, y1, mid_x, y2, x2, y2)


def mind_parent(c, x, y, w, h, title, body, accent, tint):
    rounded_box(c, x, y, w, h, WHITE, accent, radius=12, stroke_width=1.4)
    c.setFillColor(tint)
    c.roundRect(x + 10, y + h - 25, w - 20, 16, 8, fill=1, stroke=0)
    paragraph(c, title, x + 16, y + h - 27, w - 32, 18, 8.5, accent, True, 9.5)
    paragraph(c, body, x + 14, y + 10, w - 28, h - 40, 6.7, MUTED, False, 8.2)


def mind_child(c, text, x, y, w, accent, tint):
    rounded_box(c, x, y, w, 22, tint, tint, radius=7, stroke_width=0.5)
    c.setFillColor(accent)
    c.circle(x + 10, y + 11, 2.4, fill=1, stroke=0)
    paragraph(c, text, x + 18, y + 4, w - 24, 14, 6.2, INK, True, 7)


def draw_mindmap_page(c):
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    margin = 34

    c.setFillColor(NAVY)
    c.rect(0, PAGE_H - 86, PAGE_W, 86, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.circle(margin + 8, PAGE_H - 32, 8, fill=1, stroke=0)
    c.setFont(FONT_BOLD, 8)
    c.setFillColor(colors.HexColor("#93E0D4"))
    c.drawString(margin + 24, PAGE_H - 35, "PARAMETER ARCHITECTURE MIND MAP")
    c.setFont(FONT_BOLD, 22)
    c.setFillColor(WHITE)
    c.drawString(margin, PAGE_H - 62, "Lamuri x PlatformBelajar Pro")
    c.setFont(FONT, 9)
    c.setFillColor(colors.HexColor("#C9D3E7"))
    c.drawString(margin + 370, PAGE_H - 60, "One ecosystem, clear responsibilities")
    pill(c, "PAGE 1 / MIND MAP", PAGE_W - 154, PAGE_H - 49, 120, colors.HexColor("#243457"), colors.HexColor("#CFE0FF"))

    summary_y = PAGE_H - 151
    rounded_box(c, margin, summary_y, PAGE_W - 2 * margin, 48, WHITE, LINE, radius=12)
    c.setFillColor(TEAL)
    c.roundRect(margin, summary_y, 8, 48, 4, fill=1, stroke=0)
    paragraph(
        c,
        "<b>Big picture:</b> Lamuri adalah wajah komersial dan experience brand. PlatformBelajar Pro adalah mesin operasionalnya. "
        "Seluruh kelas, akun, pembayaran, enrollment, dan aktivitas belajar bertemu pada satu integration core yang dimiliki Parameter.",
        margin + 22,
        summary_y + 9,
        PAGE_W - 2 * margin - 44,
        29,
        8.6,
        INK,
        False,
        11,
    )

    # Connections are drawn first so every node stays visually on top.
    cx, cy, cw, ch = 475, 385, 240, 100
    center_points = {
        "api": (cx + cw / 2, cy + ch),
        "content": (cx, cy + 70),
        "storefront": (cx + cw, cy + 70),
        "governance": (cx, cy + 28),
        "commerce": (cx + cw, cy + 28),
        "lms": (cx + cw / 2, cy),
    }
    parent_points = {
        "api": (595, 585),
        "content": (415, 551),
        "storefront": (775, 551),
        "governance": (415, 331),
        "commerce": (775, 331),
        "lms": (595, 282),
    }
    branch_colors = {
        "api": BLUE,
        "content": PURPLE,
        "storefront": CORAL,
        "governance": AMBER,
        "commerce": GREEN,
        "lms": TEAL,
    }
    for key in center_points:
        curved_connector(c, *center_points[key], *parent_points[key], branch_colors[key], 3)

    # Child connectors.
    for yy in (604, 569, 534, 499):
        curved_connector(c, 185, 551, 160, yy + 11, PURPLE, 1)
    for yy in (604, 569, 534, 499):
        curved_connector(c, 1005, 551, 1030, yy + 11, CORAL, 1)
    for yy in (384, 349, 314, 279):
        curved_connector(c, 165, 331, 145, yy + 11, AMBER, 1)
    for yy in (384, 349, 314, 279):
        curved_connector(c, 1005, 331, 1030, yy + 11, GREEN, 1)
    for xx in (377, 486, 595, 704):
        curved_connector(c, 595, 653, xx + 48, 668, BLUE, 1)
    for xx in (377, 486, 595, 704):
        curved_connector(c, 595, 210, xx + 48, 181, TEAL, 1)

    # Central node.
    c.setFillColor(NAVY)
    c.setStrokeColor(NAVY)
    c.roundRect(cx, cy, cw, ch, 18, fill=1, stroke=1)
    pill(c, "SOURCE OF TRUTH", cx + 65, cy + ch - 28, 110, colors.HexColor("#243457"), colors.HexColor("#CFE0FF"))
    paragraph(c, "INTEGRATION CORE", cx + 28, cy + 38, cw - 56, 24, 14, WHITE, True, 16)
    paragraph(c, "Identity + content + commerce + learning", cx + 28, cy + 18, cw - 56, 18, 7.4, colors.HexColor("#C9D3E7"), False, 9)

    # Parent branches.
    mind_parent(c, 495, 585, 200, 68, "PUBLIC CONTENT API", "Katalog Lamuri dibaca dari PlatformBelajar dan diperbarui berkala.", BLUE, BLUE_TINT)
    mind_parent(c, 185, 515, 230, 72, "CONTENT & CMS", "Instruktur Lamuri mengelola kelas sekali dari portal PlatformBelajar.", PURPLE, PURPLE_TINT)
    mind_parent(c, 775, 515, 230, 72, "LAMURI STOREFRONT", "Brand discovery, narasi kelas, jadwal, dan conversion entry point.", CORAL, CORAL_TINT)
    mind_parent(c, 165, 295, 250, 72, "SCOPE & GOVERNANCE", "Kelas Marketplace tetap terikat Parameter, namun terpisah dari katalog internal.", AMBER, AMBER_TINT)
    mind_parent(c, 775, 295, 230, 72, "COMMERCE & MAYAR", "Checkout dibuat oleh PlatformBelajar; settlement dikonfirmasi melalui webhook.", GREEN, GREEN_TINT)
    mind_parent(c, 495, 210, 200, 72, "ENROLLMENT & LMS", "Pembayaran valid berujung pada membership dan akses belajar otomatis.", TEAL, TEAL_TINT)

    # Child nodes.
    for text, yy in zip(("Lamuri-only form", "Class + sessions", "Banner + copy", "PostgreSQL"), (604, 569, 534, 499)):
        mind_child(c, text, 45, yy, 115, PURPLE, PURPLE_TINT)
    for text, yy in zip(("lamuri.parameter.cloud", "Course detail", "Session selector", "Redirect source=lamuri"), (604, 569, 534, 499)):
        mind_child(c, text, 1030, yy, 125, CORAL, CORAL_TINT)
    for text, yy in zip(("marketplace_listing", "Exact account + org", "Internal catalog excluded", "Secrets omitted"), (384, 349, 314, 279)):
        mind_child(c, text, 35, yy, 110, AMBER, AMBER_TINT)
    for text, yy in zip(("Login before payment", "Purchase ID", "Mayar invoice", "Payment webhook"), (384, 349, 314, 279)):
        mind_child(c, text, 1030, yy, 125, GREEN, GREEN_TINT)
    for text, xx in zip(("Published only", "60s cache", "Course endpoint", "Shared IDs"), (377, 486, 595, 704)):
        mind_child(c, text, xx, 657, 96, BLUE, BLUE_TINT)
    for text, xx in zip(("class_students", "Parameter member", "My Courses", "Tasks + forum"), (377, 486, 595, 704)):
        mind_child(c, text, xx, 169, 96, TEAL, TEAL_TINT)

    # Embedded roadmap.
    roadmap_y = 51
    roadmap_h = 93
    rounded_box(c, margin, roadmap_y, PAGE_W - 2 * margin, roadmap_h, WHITE, LINE, radius=12)
    paragraph(c, "ROADMAP", margin + 16, roadmap_y + 57, 86, 20, 9, GREEN, True, 10)
    paragraph(c, "Dari terintegrasi<br/>menjadi observable", margin + 16, roadmap_y + 20, 95, 34, 7, MUTED, False, 9)
    phases = [
        ("LIVE", "Integrated foundation", "CMS, catalog API, Mayar, auto-enrollment", GREEN, GREEN_TINT),
        ("NEXT", "Reliability hardening", "Central scope policy, signed service access", BLUE, BLUE_TINT),
        ("30-60 DAYS", "Operational visibility", "Sync health, webhook replay, alerting", AMBER, AMBER_TINT),
        ("SCALE", "Growth intelligence", "Attribution, funnel, cohort performance", PURPLE, PURPLE_TINT),
    ]
    phase_x = margin + 122
    phase_gap = 10
    phase_w = (PAGE_W - margin - phase_x - phase_gap * 3) / 4
    for idx, (tag, title, detail, accent, tint) in enumerate(phases):
        px = phase_x + idx * (phase_w + phase_gap)
        rounded_box(c, px, roadmap_y + 12, phase_w, roadmap_h - 24, tint, tint, radius=9)
        pill(c, tag, px + 10, roadmap_y + roadmap_h - 33, 64 if idx != 2 else 78, WHITE, accent)
        paragraph(c, title, px + 11, roadmap_y + 28, phase_w - 22, 21, 7.8, INK, True, 9)
        paragraph(c, detail, px + 11, roadmap_y + 8, phase_w - 22, 20, 6.2, MUTED, False, 7.4)

    c.setFont(FONT, 6.4)
    c.setFillColor(MUTED)
    c.drawString(margin, 25, "Prepared for Parameter - executive architecture view")
    c.drawRightString(PAGE_W - margin, 25, "Details continue on page 2 | Credentials and secrets intentionally omitted")


def draw_document():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUTPUT), pagesize=(PAGE_W, PAGE_H))
    c.setTitle("Lamuri x PlatformBelajar Pro - Architecture Mind Map and Integration Canvas")
    c.setAuthor("Parameter")
    c.setSubject("Visualisasi framework integrasi website Lamuri, PlatformBelajar Pro, dan Mayar")

    draw_mindmap_page(c)
    c.showPage()

    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    margin = 34

    # Header
    c.setFillColor(NAVY)
    c.rect(0, PAGE_H - 86, PAGE_W, 86, fill=1, stroke=0)
    c.setFillColor(CORAL)
    c.circle(margin + 8, PAGE_H - 32, 8, fill=1, stroke=0)
    c.setFont(FONT_BOLD, 8)
    c.setFillColor(colors.HexColor("#F9B6A6"))
    c.drawString(margin + 24, PAGE_H - 35, "PARAMETER INFRASTRUCTURE NOTE")
    c.setFont(FONT_BOLD, 22)
    c.setFillColor(WHITE)
    c.drawString(margin, PAGE_H - 62, "Lamuri x PlatformBelajar Pro")
    c.setFont(FONT, 9)
    c.setFillColor(colors.HexColor("#C9D3E7"))
    c.drawString(margin + 370, PAGE_H - 60, "Integration Architecture Canvas")
    pill(c, "PAGE 2 / FLOW", PAGE_W - 196, PAGE_H - 49, 82, colors.HexColor("#243457"), colors.HexColor("#CFE0FF"))
    pill(c, "15 JUL 2026", PAGE_W - 105, PAGE_H - 49, 72, CORAL, WHITE)

    # Executive summary
    summary_y = PAGE_H - 151
    rounded_box(c, margin, summary_y, PAGE_W - 2 * margin, 48, WHITE, LINE, radius=12)
    c.setFillColor(BLUE)
    c.roundRect(margin, summary_y, 8, 48, 4, fill=1, stroke=0)
    paragraph(
        c,
        "<b>Operating principle:</b> PlatformBelajar Pro adalah source of truth untuk katalog, transaksi, identitas, dan aktivitas belajar. "
        "Lamuri berperan sebagai branded storefront. Mayar memproses pembayaran, lalu webhook PlatformBelajar memberikan akses LMS secara otomatis.",
        margin + 22,
        summary_y + 9,
        PAGE_W - 2 * margin - 44,
        29,
        8.6,
        INK,
        False,
        11,
    )

    # Main architecture canvas
    c.setFont(FONT_BOLD, 12)
    c.setFillColor(INK)
    c.drawString(margin, summary_y - 26, "End-to-end integration flow")
    c.setFont(FONT, 7.2)
    c.setFillColor(MUTED)
    c.drawRightString(PAGE_W - margin, summary_y - 24, "Solid arrows = synchronous hand-off | Webhook = asynchronous settlement")

    label_w = 126
    flow_x = margin + label_w + 18
    flow_w = PAGE_W - margin - flow_x
    gap = 13
    card_w = (flow_w - gap * 4) / 5
    lane_h = 84
    lane_ys = [summary_y - 130, summary_y - 226, summary_y - 322]

    # Lane 1: Content supply
    y = lane_ys[0]
    lane_label(c, margin, y, label_w, lane_h, "01  CONTENT", "Satu kali input. Dua kanal publikasi.", BLUE, BLUE_TINT)
    lane1 = [
        ("Lamuri Publisher", "Akun khusus Lamuri di lembaga Parameter membuat atau mengubah kelas.", "IDENTITY GATE"),
        ("Course CMS", "Form khusus mengelola judul, banner, narasi, outcome, tools, format, harga, dan jadwal.", "PLATFORMBELAJAR"),
        ("Learning Data", "Classes, sessions, meetings, Lamuri profile, instructor, dan status publish tersimpan terpusat.", "POSTGRESQL"),
        ("Public Read API", "Endpoint Lamuri menyajikan kelas aktif dan terbit dengan cache 60 detik.", "READ-ONLY API"),
        ("Lamuri Website", "Halaman kelas merender katalog terbaru; fallback lokal menjaga halaman tetap tersedia.", "BRANDED STOREFRONT"),
    ]
    for i, (title, body, meta) in enumerate(lane1):
        x = flow_x + i * (card_w + gap)
        flow_card(c, x, y, card_w, lane_h, i + 1, title, body, BLUE, BLUE_TINT, meta)
        if i < 4:
            arrow(c, x + card_w + 2, y + lane_h / 2, x + card_w + gap - 2, y + lane_h / 2, BLUE)

    # Lane 2: Buyer journey
    y = lane_ys[1]
    lane_label(c, margin, y, label_w, lane_h, "02  CUSTOMER", "Discovery di Lamuri. Identity di LMS.", CORAL, CORAL_TINT)
    lane2 = [
        ("Visitor", "Calon peserta menemukan kelas lewat halaman Lamuri dan memilih jadwal.", "DISCOVERY"),
        ("Course Detail", "Lamuri membawa class ID dan session ID yang sama dengan PlatformBelajar.", "SHARED IDENTIFIER"),
        ("Marketplace", "Pengunjung dialihkan ke halaman kelas PlatformBelajar dengan source=lamuri.", "REDIRECT"),
        ("Login / Register", "Akun diperlukan sebelum checkout agar pembayaran dapat diikat ke student yang tepat.", "AUTH REQUIRED"),
        ("Checkout Mayar", "Platform membuat invoice berdasarkan kelas, harga, customer, dan purchase ID.", "HOSTED PAYMENT"),
    ]
    for i, (title, body, meta) in enumerate(lane2):
        x = flow_x + i * (card_w + gap)
        flow_card(c, x, y, card_w, lane_h, i + 1, title, body, CORAL, CORAL_TINT, meta)
        if i < 4:
            arrow(c, x + card_w + 2, y + lane_h / 2, x + card_w + gap - 2, y + lane_h / 2, CORAL)

    # Lane 3: Settlement and access
    y = lane_ys[2]
    lane_label(c, margin, y, label_w, lane_h, "03  ACCESS", "Payment settled. Learning unlocked.", TEAL, TEAL_TINT)
    lane3 = [
        ("Payment Received", "Mayar mengirim event pembayaran ke webhook PlatformBelajar.", "ASYNC EVENT"),
        ("Webhook Guard", "Shared token, transaction reference, dan status pending mencegah pemrosesan palsu atau ganda.", "VALIDATE"),
        ("Purchase Record", "Transaksi ditandai paid; revenue split dan instructor earning dicatat.", "SETTLEMENT"),
        ("Parameter Member", "Buyer baru dihubungkan ke Parameter tanpa menimpa membership lembaga lain.", "ORG BINDING"),
        ("LMS Access", "class_students dibuat; kelas muncul di My Courses beserta materi, tugas, forum, dan progress.", "ENROLLED"),
    ]
    for i, (title, body, meta) in enumerate(lane3):
        x = flow_x + i * (card_w + gap)
        flow_card(c, x, y, card_w, lane_h, i + 1, title, body, TEAL, TEAL_TINT, meta)
        if i < 4:
            arrow(c, x + card_w + 2, y + lane_h / 2, x + card_w + gap - 2, y + lane_h / 2, TEAL)

    # Bottom cards
    bottom_y = 55
    bottom_h = 194
    col_gap = 14
    col1 = 350
    col2 = 340
    col3 = PAGE_W - 2 * margin - col_gap * 2 - col1 - col2
    x1 = margin
    x2 = x1 + col1 + col_gap
    x3 = x2 + col2 + col_gap

    section_card(c, x1, bottom_y, col1, bottom_h, "Boundary rules", "Marketplace tetap terpisah dari katalog internal", PURPLE, PURPLE_TINT)
    bullet(c, "<b>marketplace_listing = 1</b> menjadi penanda eksplisit kelas Lamuri yang dijual publik.", x1 + 14, bottom_y + 112, col1 - 28, INK, PURPLE)
    bullet(c, "Organization ID Parameter tetap dipertahankan untuk membership otomatis setelah pembayaran.", x1 + 14, bottom_y + 80, col1 - 28, INK, PURPLE)
    bullet(c, "Kelas Marketplace tidak tampil di Pilih Kelas Baru atau Katalog Lembaga Parameter.", x1 + 14, bottom_y + 48, col1 - 28, INK, PURPLE)
    bullet(c, "Katalog lembaga hanya memuat kelas <b>Internal + aktif + berbayar</b>; buyer Marketplace tetap melihat kelasnya di My Courses.", x1 + 14, bottom_y + 14, col1 - 28, INK, PURPLE)

    section_card(c, x2, bottom_y, col2, bottom_h, "Control plane", "Siapa mengelola apa", AMBER, AMBER_TINT)
    controls = [
        ("Lamuri Publisher", "Konten kelas, banner, harga, jadwal, publish"),
        ("PlatformBelajar", "Identity, katalog, transaksi, enrollment, LMS"),
        ("Mayar", "Invoice, kanal pembayaran, payment event"),
        ("Admin Parameter", "Membership, operasi student, dukungan kasus"),
    ]
    cy = bottom_y + 116
    for idx, (owner, role) in enumerate(controls):
        c.setFillColor([BLUE, TEAL, CORAL, PURPLE][idx])
        c.roundRect(x2 + 14, cy - idx * 30, 86, 20, 6, fill=1, stroke=0)
        c.setFont(FONT_BOLD, 6.2)
        c.setFillColor(WHITE)
        c.drawCentredString(x2 + 57, cy + 6.2 - idx * 30, owner)
        paragraph(c, role, x2 + 110, cy - 1 - idx * 30, col2 - 126, 22, 6.8, MUTED, False, 8.2)

    section_card(c, x3, bottom_y, col3, bottom_h, "Roadmap", "From integrated to observable", GREEN, GREEN_TINT)
    roadmap = [
        ("LIVE", "Integrated foundation", "CMS, API catalog, redirect checkout, webhook, auto-enrollment", GREEN),
        ("NEXT", "Reliability hardening", "Central publish-scope policy, signed service access, webhook replay", BLUE),
        ("30-60D", "Operational visibility", "Sync health, failed-payment queue, alerting, audit dashboard", AMBER),
        ("SCALE", "Growth intelligence", "Lamuri funnel, attribution, cohort performance, campaign insights", PURPLE),
    ]
    ry = bottom_y + 123
    for idx, (phase, title, detail, accent) in enumerate(roadmap):
        yy = ry - idx * 34
        c.setFillColor(accent)
        c.circle(x3 + 18, yy + 5, 5, fill=1, stroke=0)
        if idx < len(roadmap) - 1:
            c.setStrokeColor(LINE)
            c.setLineWidth(1.2)
            c.line(x3 + 18, yy, x3 + 18, yy - 25)
        pill(c, phase, x3 + 31, yy - 4, 47, colors.Color(accent.red, accent.green, accent.blue, alpha=0.12), accent)
        paragraph(c, f"<b>{title}</b><br/><font color='#5F6B7A'>{detail}</font>", x3 + 87, yy - 5, col3 - 102, 30, 6.5, INK, False, 7.8)

    # Footer
    c.setStrokeColor(LINE)
    c.setLineWidth(0.8)
    c.line(margin, 38, PAGE_W - margin, 38)
    c.setFont(FONT, 6.4)
    c.setFillColor(MUTED)
    c.drawString(margin, 24, "Prepared for Parameter - architecture derived from the current Lamuri and PlatformBelajar Pro implementation")
    c.drawRightString(PAGE_W - margin, 24, "Credentials and secrets intentionally omitted | lamuri.parameter.cloud | pro.platformbelajar.my.id")

    c.showPage()
    c.save()


if __name__ == "__main__":
    draw_document()
    print(OUTPUT)
