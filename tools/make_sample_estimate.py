#!/usr/bin/env python3
"""Rebuild sample-estimate.pdf — the priced, 2-page portfolio sample.

Why this file exists: the previous sample-estimate.pdf was produced from a
generator that was never kept, so its header still carried an old address. This
script is the source of truth for that document from now on: every printed
token lives in CONTENT below, and the renderer only decides geometry.

Rules this file is written to satisfy:
  * support@olcontrol.com is the only address; no personal alias anywhere.
  * Every figure, date, registration number, reference and limitation sentence
    is reproduced exactly as printed before — nothing invented, no new price,
    no discount, no credential claim.
  * Letter paper, exactly 2 pages, dark text on white, mono for figures.

    python3 tools/make_sample_estimate.py           # writes ../sample-estimate.pdf
"""
import os

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "sample-estimate.pdf")

# ── palette: the site's own role tokens (site.css :root) ────────────────────
NAVY = HexColor("#183A5C")
STEEL = HexColor("#315D8C")
INK = HexColor("#1D232B")
TEXT2 = HexColor("#3B4550")
MUTED = HexColor("#6C7177")
RULE = HexColor("#D5DCE3")
HAIR = HexColor("#E1E7ED")
WASH = HexColor("#F4F6F9")
GOLD = HexColor("#B8860B")
WHITE = HexColor("#FFFFFF")

# ── type: serif display, sans reading, mono figures (site type system) ──────
FONTS = [
    ("Georgia", "/System/Library/Fonts/Supplemental/Georgia.ttf", None),
    ("Georgia-Bold", "/System/Library/Fonts/Supplemental/Georgia Bold.ttf", None),
    ("Georgia-Italic", "/System/Library/Fonts/Supplemental/Georgia Italic.ttf", None),
    ("Menlo", "/System/Library/Fonts/Menlo.ttc", 0),
    ("Menlo-Bold", "/System/Library/Fonts/Menlo.ttc", 1),
]
SANS, SANS_B = "Helvetica", "Helvetica-Bold"
SANS_I = "Helvetica-Oblique"

# ── every printed token, exactly as the document must print it ──────────────
CONTENT = {
    "brand": "OL — Optimization and Logistics",
    "tagline": "ESTIMATING • TAKEOFFS • DOCUMENT WORK",
    "place": "Montréal, Québec, Canada",
    "email": "support@olcontrol.com",
    "site": "ol-projects.github.io/ol-services",
    "regs": "NEQ 2270669312 • GST 81902 9992 RT0001 • QST 4024451921 TQ0002",
    "notice": "SAMPLE — NOT A BINDING QUOTE",
    "estimate_no": "SAMPLE-2026-001",
    "date_issued": "November 06, 2026",
    "valid_until": "December 06, 2026",
    "revision": "Rev. 0",
    "title": "Bathroom Renovation — 120 sq ft",
    "project": [
        ("Project Name:", "Sample Bathroom Renovation"),
        ("Site Address:", "Sample address — Montreal, QC"),
        ("Unit Area:", "Approx. 120 sq ft"),
        ("Scope Basis:", "Dimensions supplied by the client; no site visit performed"),
    ],
    "client": [
        ("Prepared For:", "Sample Client Inc. (illustrative)"),
        ("Attention:", "—"),
        ("Client Type:", "Residential renovation"),
        ("Address:", "Montreal, QC"),
    ],
    "scope": "SCOPE OF WORK",
    "columns": ("REF.", "DESCRIPTION OF WORK", "QTY", "VALUE (CAD)"),
    "page1": [
        ("DIVISION 02 - SELECTIVE DEMOLITION & REMOVALS", [
            ("02.1", "Strip-out of the existing bathroom",
             "Remove existing tile, vanity, toilet, tub and drywall to the studs. "
             "Protect the corridor and stairwell. Include debris removal and disposal.",
             "1", "$1,850.00"),
        ]),
        ("DIVISION 22 - PLUMBING", [
            ("22.1", "Relocate and rough-in the new fixtures",
             "Relocate the shower drain, rough-in the new vanity and toilet per plan. "
             "Supply and install shut-off valves. Pressure-test and certify.",
             "1", "$2,400.00"),
        ]),
        ("DIVISION 26 - ELECTRICAL", [
            ("26.1", "Circuits, GFCI protection and fixtures",
             "Two dedicated circuits, GFCI receptacles, vanity sconce and ceiling fan "
             "rated box. Permit included; inspection coordinated.",
             "1", "$1,650.00"),
        ]),
        ("DIVISION 09 - TILING & WATERPROOFING", [
            ("09.1", "Cement board and bonded waterproofing membrane",
             "1/2\" cement board on walls and floor, seams taped, two-coat waterproof "
             "membrane with banding at all corners and the shower pan.",
             "1", "$980.00"),
            ("09.2", "Porcelain tile supply — walls and floor",
             "120 sq ft of 600x1200 porcelain plus 12% waste allowance. Client may "
             "substitute any in-stock SKU at the same price.",
             "120", "$7.25"),
            ("09.3", "Tile installation, walls and floor",
             "Large-format installation with levelling system, epoxy grout in the wet "
             "area, silicone at all movement joints, 1/8\" joints.",
             "120", "$19.00"),
        ]),
    ],
    "page2": [
        ("DIVISION 10 - FIXTURES & FINISHES", [
            ("10.1", "Vanity, toilet and shower fixtures",
             "Supply and install a 36\" vanity with quartz top, a comfort-height toilet "
             "and a thermostatic shower valve with trim. Allowance included.",
             "1", "$2,850.00"),
            ("10.2", "Paint and finishing",
             "Patch, sand, primer and two coats on walls and ceiling in the bathroom and "
             "the adjacent hallway patch.",
             "1", "$720.00"),
        ]),
    ],
    "totals": [
        ("Subtotal (before taxes)", "$13,600.00"),
        ("GST - Goods & Services Tax (5.0%)", "$680.00"),
        ("QST - Québec Sales Tax (9.975%)", "$1,356.60"),
    ],
    "total_label": "ESTIMATED TOTAL (taxes included)",
    "total": "$15,636.60",
    "terms_title": "TERMS & CONDITIONS",
    "terms": [
        ("What this document is:",
         "A portfolio sample prepared by OL to show the format and level of detail of "
         "an estimating deliverable. It is not an offer for construction work and no "
         "price in it is binding."),
        ("Scope Basis:",
         "Priced from the dimensions and selections supplied. A site visit, a plan "
         "review or a material substitution changes the numbers."),
        ("Exclusions:",
         "Permits other than the electrical permit, structural work, asbestos or mould "
         "abatement, and any work not listed in the scope."),
        ("Validity:",
         "Thirty days from the issue date, for the sample only."),
    ],
    "sign_left": ("ACCEPTED — CLIENT",
                  ["Signature: __________________________________",
                   "Print name: _________________________________",
                   "Date: __________________"]),
    "sign_right": ("PREPARED BY — OL",
                   ["Signature: __________________________________",
                    "Name: _________________________________ OL",
                    "Date: __________________ 2026-11-06"]),
    "foot_title": ("OL — Optimization and Logistics | Montréal, QC | NEQ 2270669312 | "
                   "GST 81902 9992 RT0001 | QST 4024451921 TQ0002"),
    "foot_note": "Sample document — portfolio piece, not a binding quote",
}

# ── geometry ────────────────────────────────────────────────────────────────
PW, PH = letter              # 612 x 792
ML, MR = 54.0, 54.0
RIGHT = PW - MR              # 558
CW = RIGHT - ML              # 504


def register_fonts():
    for name, path, idx in FONTS:
        if not os.path.exists(path):
            raise SystemExit(f"missing font: {path}")
        if idx is None:
            pdfmetrics.registerFont(TTFont(name, path))
        else:
            pdfmetrics.registerFont(TTFont(name, path, subfontIndex=idx))


def sw(text, font, size):
    return pdfmetrics.stringWidth(text, font, size)


def wrap(text, font, size, width):
    """Greedy wrap; returns lines that each fit `width`."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if sw(trial, font, size) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def wrap_hanging(text, font, size, first_w, rest_w):
    """Wrap with a first-line indent: line 0 fits `first_w`, the rest `rest_w`."""
    words = text.split()
    lines, cur, width = [], "", first_w
    for w in words:
        trial = f"{cur} {w}".strip()
        if sw(trial, font, size) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur, width = w, rest_w
    if cur:
        lines.append(cur)
    return lines


def tracked(c, text, x, y, font, size, color, tracking=0.0, align="left"):
    """Letter-spaced text (small caps labels). align: left|right|center."""
    w = sw(text, font, size) + tracking * max(len(text) - 1, 0)
    if align == "right":
        x -= w
    elif align == "center":
        x -= w / 2
    t = c.beginText(x, y)
    t.setFont(font, size)
    t.setFillColor(color)
    t.setCharSpace(tracking)
    t.textOut(text)
    t.setCharSpace(0)          # Tc lives in the graphics state: never let it leak
    c.drawText(t)
    return w


def para(c, text, x, y, width, font, size, leading, color):
    """Draw a wrapped paragraph top-down; returns the y below its last line."""
    c.setFont(font, size)
    c.setFillColor(color)
    for line in wrap(text, font, size, width):
        c.drawString(x, y, line)
        y -= leading
    return y


# ── page furniture ──────────────────────────────────────────────────────────
def footer(c, page, pages=2):
    y = 64
    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.line(ML, y, RIGHT, y)
    tracked(c, CONTENT["foot_title"], PW / 2, y - 11, SANS, 6.2, MUTED, 0.1, "center")
    tracked(c, CONTENT["foot_note"], PW / 2, y - 21.5, SANS_I, 6.6, MUTED, 0.1, "center")
    tracked(c, f"Sample No. {CONTENT['estimate_no']} | Rev. 0 | Page {page} of {pages}",
            PW / 2, y - 32, "Menlo", 6.3, STEEL, 0.1, "center")


def header(c):
    top = PH - 40

    # wordmark + descriptor
    c.setFont("Georgia-Bold", 19)
    c.setFillColor(NAVY)
    c.drawString(ML, top, "OL")
    w = sw("OL", "Georgia-Bold", 19)
    c.setFont(SANS_B, 11.2)
    c.setFillColor(NAVY)
    c.drawString(ML + w + 2, top + 0.5, "— Optimization and Logistics")

    tracked(c, CONTENT["tagline"], ML, top - 13, "Menlo", 6.5, STEEL, 0.55)
    c.setFont(SANS, 8.4)
    c.setFillColor(INK)
    c.drawString(ML, top - 26, CONTENT["place"])

    y = top - 39
    c.setFont(SANS_B, 8.4)
    c.setFillColor(NAVY)
    c.drawString(ML, y, CONTENT["email"])
    ew = sw(CONTENT["email"], SANS_B, 8.4)
    c.setFont(SANS, 8.4)
    c.setFillColor(STEEL)
    c.drawString(ML + ew, y, "  |  " + CONTENT["site"])

    tracked(c, CONTENT["regs"], ML, y - 12, "Menlo", 6.2, MUTED, 0.04)

    # right block: notice + estimate identity
    tracked(c, CONTENT["notice"], RIGHT, top + 1, SANS_B, 7.4, NAVY, 1.15, "right")
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.6)
    c.line(RIGHT - 152, top - 4.5, RIGHT, top - 4.5)

    rows = [("Estimate No.:", CONTENT["estimate_no"]),
            ("Date Issued:", CONTENT["date_issued"]),
            ("Valid Until:", CONTENT["valid_until"]),
            ("Revision:", CONTENT["revision"])]
    ry = top - 19
    for label, value in rows:
        tracked(c, label, RIGHT - 92, ry, SANS, 6.6, MUTED, 0.35, "right")
        c.setFont("Menlo", 7.9)
        c.setFillColor(INK)
        c.drawRightString(RIGHT, ry, value)
        ry -= 12.6

    # header rule sits below the lower of the two columns
    ry = min(ry, y - 12) - 10
    c.setStrokeColor(RULE)
    c.setLineWidth(0.8)
    c.line(ML, ry, RIGHT, ry)
    return ry


def panel(c, x, y, w, h, title, rows, label_w=58, pad=9, value_w=None):
    c.setFillColor(WHITE)
    c.setStrokeColor(HAIR)
    c.setLineWidth(0.7)
    c.rect(x, y, w, h, stroke=1, fill=1)
    c.setFillColor(NAVY)
    c.rect(x, y, 2.2, h, stroke=0, fill=1)

    tracked(c, title, x + pad, y + h - 13, "Menlo-Bold", 6.4, STEEL, 0.7)
    c.setStrokeColor(HAIR)
    c.setLineWidth(0.6)
    c.line(x + pad, y + h - 19, x + w - pad, y + h - 19)

    ty = y + h - 32
    vw = value_w if value_w else (w - label_w - pad * 1.7)
    for label, value in rows:
        c.setFont(SANS, 7.0)
        c.setFillColor(MUTED)
        for i, line in enumerate(wrap(label, SANS, 7.0, label_w - 4)):
            c.drawString(x + pad, ty - i * 8, line)
        ty = para(c, value, x + pad + label_w, ty, vw, SANS, 8.1, 9.8, INK) - 3.2
    return ty


def table_head(c, y, h=15):
    c.setFillColor(WASH)
    c.rect(ML, y, CW, h, stroke=0, fill=1)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.7)
    c.line(ML, y, RIGHT, y)
    c.line(ML, y + h, RIGHT, y + h)
    base = y + 4.6
    ref, desc, qty, val = CONTENT["columns"]
    tracked(c, ref, ML + 8, base, "Menlo-Bold", 6.3, STEEL, 0.6)
    tracked(c, desc, X_DESC, base, "Menlo-Bold", 6.3, STEEL, 0.6)
    tracked(c, qty, X_QTY, base, "Menlo-Bold", 6.3, STEEL, 0.6, "right")
    tracked(c, val, X_VAL, base, "Menlo-Bold", 6.3, STEEL, 0.6, "right")
    return y - h


X_REF = ML + 8
X_DESC = ML + 52
X_QTY = RIGHT - 88
X_VAL = RIGHT - 8


def division(c, y, name):
    c.setStrokeColor(RULE)
    c.setLineWidth(0.7)
    c.line(ML, y, RIGHT, y)
    tracked(c, name, ML + 8, y - 12, SANS_B, 7.2, NAVY, 0.75)
    return y - 18


def item(c, y, ref, title, desc, qty, value):
    c.setFont("Menlo", 7.6)
    c.setFillColor(STEEL)
    c.drawString(X_REF, y - 12, ref)

    c.setFont(SANS_B, 8.7)
    c.setFillColor(INK)
    c.drawString(X_DESC, y - 12, title)

    c.setFont("Menlo", 8.4)
    c.setFillColor(INK)
    c.drawRightString(X_QTY, y - 12, qty)
    c.drawRightString(X_VAL, y - 12, value)

    y = para(c, desc, X_DESC, y - 23.5, X_QTY - X_DESC - 46, SANS, 7.7, 9.6, TEXT2)
    return y - 5


def totals(c, y):
    x0, x1 = 322.0, RIGHT
    c.setStrokeColor(RULE)
    c.setLineWidth(0.7)
    c.line(x0, y, x1, y)

    for label, value in CONTENT["totals"]:
        c.setFont(SANS, 8.5)
        c.setFillColor(TEXT2)
        c.drawString(x0, y - 15, label)
        c.setFont("Menlo", 8.8)
        c.setFillColor(INK)
        c.drawRightString(x1, y - 15, value)
        c.setStrokeColor(HAIR)
        c.setLineWidth(0.55)
        c.line(x0, y - 23, x1, y - 23)
        y -= 24

    # total band
    y -= 8
    bh = 40
    c.setFillColor(NAVY)
    c.rect(x0, y - bh + 6, x1 - x0, bh, stroke=0, fill=1)
    tracked(c, "ESTIMATED TOTAL", x0 + 12, y - 6, "Menlo-Bold", 6.6, HexColor("#BFD6EC"), 0.7)
    tracked(c, "(taxes included)", x0 + 12, y - 16, SANS, 7.6, HexColor("#E4EDF5"), 0.1)
    c.setFont("Menlo-Bold", 13.2)
    c.setFillColor(WHITE)
    c.drawRightString(x1 - 12, y - 13, CONTENT["total"])
    return y - bh - 4


def terms(c, y):
    tracked(c, CONTENT["terms_title"], ML, y, "Menlo-Bold", 7.0, NAVY, 0.8)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.7)
    c.line(ML, y - 7, RIGHT, y - 7)
    y -= 20
    for lead, body in CONTENT["terms"]:
        c.setFont("Georgia", 9)
        c.setFillColor(GOLD)
        c.drawString(ML + 1, y, "▪")
        c.setFont(SANS_B, 7.9)
        c.setFillColor(INK)
        c.drawString(ML + 15, y, lead)
        lw = sw(lead + " ", SANS_B, 7.9)
        c.setFont(SANS, 7.8)
        c.setFillColor(TEXT2)
        for i, line in enumerate(wrap_hanging(body, SANS, 7.8, CW - 15 - lw, CW - 15)):
            c.drawString(ML + 15 + (lw if i == 0 else 0), y, line)
            y -= 11.0
        y -= 8.5
    return y


def signatures(c, y):
    c.setStrokeColor(RULE)
    c.setLineWidth(0.7)
    c.line(ML, y, RIGHT, y)
    y -= 18
    for i, (title, lines) in enumerate((CONTENT["sign_left"], CONTENT["sign_right"])):
        x = ML + i * 252
        tracked(c, title, x, y, "Menlo-Bold", 6.6, STEEL, 0.7)
        ly = y - 22
        for line in lines:
            c.setFont("Menlo", 7.4)
            c.setFillColor(TEXT2)
            c.drawString(x, ly, line)
            ly -= 17.5
    return y - 22 - 17.5 * 3


# ── pages ───────────────────────────────────────────────────────────────────
def page1(c):
    y = header(c) - 32

    # title
    c.setFont("Georgia-Bold", 18)
    c.setFillColor(INK)
    c.drawString(ML, y, CONTENT["title"])
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.line(ML, y - 14, ML + 40, y - 14)

    # project / client panels
    py = y - 24
    ph = 90
    panel(c, ML, py - ph, 246, ph, "PROJECT INFORMATION", CONTENT["project"], value_w=140)
    panel(c, RIGHT - 246, py - ph, 246, ph, "CLIENT / OWNER INFORMATION", CONTENT["client"])

    # scope table
    ty = py - ph - 22
    tracked(c, CONTENT["scope"], ML, ty, "Menlo-Bold", 7.4, NAVY, 0.8)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.7)
    c.line(ML + 92, ty - 2.2, RIGHT, ty - 2.2)
    ty = table_head(c, ty - 18)

    for name, items in CONTENT["page1"]:
        ty = division(c, ty - 4, name)
        for ref, title, desc, qty, value in items:
            ty = item(c, ty, ref, title, desc, qty, value)
    if ty < 88:                      # never let the table run into the footer
        raise SystemExit(f"page 1 overflows the footer: last baseline {ty:.1f} < 88")
    footer(c, 1)


def page2(c):
    # No running head: the original carried none, and repeating the estimate
    # number here would add occurrences of figures the document already prints.
    c.setStrokeColor(NAVY)
    c.setLineWidth(2)
    c.line(ML, PH - 44, RIGHT, PH - 44)

    y = table_head(c, PH - 68)
    for name, items in CONTENT["page2"]:
        y = division(c, y - 4, name)
        for ref, title, desc, qty, value in items:
            y = item(c, y, ref, title, desc, qty, value)

    y = totals(c, y - 34)
    y = terms(c, y - 30)
    # the signature strip belongs at the foot of the page, where a signer looks
    signatures(c, 215)
    footer(c, 2)


def main():
    register_fonts()
    c = canvas.Canvas(OUT, pagesize=letter, pageCompression=1)
    c.setTitle(f"Sample estimate {CONTENT['estimate_no']} — {CONTENT['title']}")
    c.setAuthor("OL — Optimization and Logistics")
    c.setSubject("Priced sample estimate — portfolio piece, not a binding quote")
    c.setCreator("OL Services — tools/make_sample_estimate.py")
    c.setKeywords("sample, estimate, takeoff, non-binding")
    page1(c)
    c.showPage()
    page2(c)
    c.showPage()
    c.save()
    print(f"wrote {OUT} ({os.path.getsize(OUT):,} bytes)")


if __name__ == "__main__":
    main()
