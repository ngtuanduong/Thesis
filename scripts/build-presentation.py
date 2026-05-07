"""
Build the 15-minute conference presentation deck (.pptx) for HTKH GV-SV 2026.

Input:
  - Plan:    documents/conference-paper/04-presentation-plan.md
  - Visuals: documents/thesis-chapters/visuals/png/*.png

Output:
  - documents/conference-paper/05-presentation.pptx  (13 slides, 16:9)

Design language:
  - 16:9 (13.333" x 7.5")
  - Background: white
  - Primary: dark navy   #0A2540
  - Accent:  orange      #FF6B35
  - Muted:   slate gray  #4A5568
  - Sans-serif: Calibri (universally available on Win/Mac/Linux PowerPoint and Google Slides)

Run:
  python scripts/build-presentation.py
"""

from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from PIL import Image

# ---------- paths ----------
ROOT = Path(__file__).resolve().parent.parent
VIS = ROOT / "documents" / "thesis-chapters" / "visuals" / "png"
OUT = ROOT / "documents" / "conference-paper" / "05-presentation.pptx"

# ---------- design tokens ----------
NAVY   = RGBColor(0x0A, 0x25, 0x40)
ORANGE = RGBColor(0xFF, 0x6B, 0x35)
SLATE  = RGBColor(0x4A, 0x55, 0x68)
LIGHT  = RGBColor(0xF7, 0xFA, 0xFC)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
MUTED  = RGBColor(0xCB, 0xD5, 0xE0)   # for borders / divider lines only
MUTED_TEXT = RGBColor(0x64, 0x74, 0x8B)  # darker gray, readable for secondary text on projector

FONT = "Calibri"
MONO = "Consolas"

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)


# ---------- helpers ----------
def add_textbox(slide, left, top, width, height, text,
                font=FONT, size=18, bold=False, italic=False,
                color=NAVY, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = Inches(0)
    tf.margin_right = Inches(0)
    tf.margin_top = Inches(0)
    tf.margin_bottom = Inches(0)
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = text
    r.font.name = font
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color
    return tb


def add_paragraphs(slide, left, top, width, height, paragraphs,
                   font=FONT, size=16, color=NAVY, align=PP_ALIGN.LEFT,
                   anchor=MSO_ANCHOR.TOP, line_spacing=1.15):
    """paragraphs = list of dicts: {text, size?, bold?, color?, italic?, mono?, indent?}"""
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = Inches(0); tf.margin_right = Inches(0)
    tf.margin_top = Inches(0);  tf.margin_bottom = Inches(0)
    for i, spec in enumerate(paragraphs):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.alignment = spec.get("align", align)
        p.line_spacing = line_spacing
        if "indent" in spec:
            p.level = spec["indent"]
        r = p.add_run()
        r.text = spec["text"]
        r.font.name = MONO if spec.get("mono") else font
        r.font.size = Pt(spec.get("size", size))
        r.font.bold = spec.get("bold", False)
        r.font.italic = spec.get("italic", False)
        r.font.color.rgb = spec.get("color", color)
    return tb


def add_rect(slide, left, top, width, height, fill_color, line_color=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid(); shape.fill.fore_color.rgb = fill_color
    if line_color is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = line_color
    shape.shadow.inherit = False
    return shape


def add_accent_bar(slide, left, top, height=Inches(0.08), width=Inches(0.9), color=ORANGE):
    return add_rect(slide, left, top, width, height, color)


def fit_image(slide, png_path: Path, left, top, max_w, max_h):
    """Place image at (left, top) and scale into (max_w, max_h) preserving aspect ratio, centered."""
    if not png_path.exists():
        # placeholder rectangle if asset is missing
        ph = add_rect(slide, left, top, max_w, max_h, LIGHT, MUTED)
        add_textbox(slide, left, top, max_w, max_h,
                    f"[missing asset: {png_path.name}]",
                    size=14, italic=True, color=SLATE,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        return ph
    with Image.open(png_path) as im:
        iw, ih = im.size
    ar_img = iw / ih
    ar_box = max_w / max_h
    if ar_img >= ar_box:
        # image is wider than box -> fit width
        w = max_w; h = int(max_w * ih / iw)
    else:
        h = max_h; w = int(max_h * iw / ih)
    cx = left + (max_w - w) // 2
    cy = top + (max_h - h) // 2
    return slide.shapes.add_picture(str(png_path), cx, cy, width=w, height=h)


def add_footer(slide, idx, total):
    # subtle bottom-left page number + bottom-right tagline
    add_textbox(slide, Inches(0.4), Inches(7.05), Inches(3.0), Inches(0.3),
                f"{idx}/{total}", size=10, color=MUTED_TEXT, align=PP_ALIGN.LEFT)
    add_textbox(slide, Inches(9.9), Inches(7.05), Inches(3.0), Inches(0.3),
                "Nguyen Tuan Duong  •  HTKH GV-SV 2026",
                size=10, italic=True, color=MUTED_TEXT, align=PP_ALIGN.RIGHT)


def add_slide_header(slide, title_text, kicker_text=None):
    """Standard top header for content slides: orange accent bar + title + optional kicker."""
    add_accent_bar(slide, Inches(0.6), Inches(0.55))
    add_textbox(slide, Inches(0.6), Inches(0.65), Inches(11.0), Inches(0.7),
                title_text, size=30, bold=True, color=NAVY)
    if kicker_text:
        add_textbox(slide, Inches(0.6), Inches(1.25), Inches(11.0), Inches(0.4),
                    kicker_text, size=14, italic=True, color=ORANGE)


# ---------- presentation ----------
prs = Presentation()
prs.slide_width = SLIDE_W
prs.slide_height = SLIDE_H

blank = prs.slide_layouts[6]   # truly blank layout
TOTAL = 13


# =======================================================================
# Slide 1 — Title
# =======================================================================
s = prs.slides.add_slide(blank)
# big navy band on left
add_rect(s, 0, 0, Inches(0.45), SLIDE_H, NAVY)
# orange accent
add_rect(s, Inches(0.6), Inches(2.0), Inches(0.9), Inches(0.1), ORANGE)

add_textbox(s, Inches(0.6), Inches(1.0), Inches(12.0), Inches(0.5),
            "HTKH GV-SV 2026  •  Student Paper Conference",
            size=14, italic=True, color=ORANGE)

add_textbox(s, Inches(0.6), Inches(2.2), Inches(12.0), Inches(2.4),
            "An Adaptive Learning Platform\nfor University Programming Courses",
            size=44, bold=True, color=NAVY)

add_textbox(s, Inches(0.6), Inches(4.2), Inches(12.0), Inches(0.6),
            "Integrating Bayesian Knowledge Tracing, Elo Rating,",
            size=22, color=SLATE)
add_textbox(s, Inches(0.6), Inches(4.7), Inches(12.0), Inches(0.6),
            "Multi-Armed Bandits, and FSRS",
            size=22, color=SLATE)

add_textbox(s, Inches(0.6), Inches(5.7), Inches(12.0), Inches(0.45),
            "Nguyễn Tuấn Dương",
            size=20, bold=True, color=NAVY)
add_textbox(s, Inches(0.6), Inches(6.1), Inches(12.0), Inches(0.4),
            "Class 1C22, Faculty of Information Technology",
            size=14, color=SLATE)
add_textbox(s, Inches(0.6), Inches(6.5), Inches(12.0), Inches(0.4),
            "Advisor: M.Sc. Bùi Quốc Khánh",
            size=14, italic=True, color=SLATE)
add_textbox(s, Inches(0.6), Inches(7.05), Inches(12.0), Inches(0.4),
            "Implementation paper with a pre-registered pilot evaluation protocol.",
            size=11, italic=True, color=ORANGE, align=PP_ALIGN.LEFT)


# =======================================================================
# Slide 2 — The 30–40% problem
# =======================================================================
s = prs.slides.add_slide(blank)
add_slide_header(s, "The 30–40% problem")

# Big number on the left
add_textbox(s, Inches(0.6), Inches(2.4), Inches(6.0), Inches(2.5),
            "30–40%", size=60, bold=True, color=ORANGE,
            align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_textbox(s, Inches(0.6), Inches(4.9), Inches(6.0), Inches(0.5),
            "Failure rate in introductory programming",
            size=18, italic=True, color=NAVY,
            align=PP_ALIGN.CENTER)
add_textbox(s, Inches(0.6), Inches(5.4), Inches(6.0), Inches(0.4),
            "(Luxton-Reilly et al., ITiCSE 2018)",
            size=12, italic=True, color=SLATE, align=PP_ALIGN.CENTER)

# Right-side message
add_paragraphs(s, Inches(7.0), Inches(2.4), Inches(5.8), Inches(4.5),
               [
                {"text": "Stable for decades.", "size": 22, "bold": True, "color": NAVY},
                {"text": " ", "size": 8},
                {"text": "Not because students lack practice material —",
                 "size": 16, "color": SLATE},
                {"text": "the gap is structural.", "size": 16, "bold": True, "color": NAVY},
                {"text": " ", "size": 12},
                {"text": "Programming skill is acquired ", "size": 16, "color": SLATE},
                {"text": "individually and through practice;",
                 "size": 16, "italic": True, "color": ORANGE},
                {"text": "it is taught ", "size": 16, "color": SLATE},
                {"text": "uniformly and at scale.",
                 "size": 16, "italic": True, "color": ORANGE},
                {"text": " ", "size": 12},
                {"text": "→ The mismatch — not the volume — is the bottleneck.",
                 "size": 17, "bold": True, "color": NAVY},
               ])
add_footer(s, 2, TOTAL)


# =======================================================================
# Slide 3 — The integration gap
# =======================================================================
s = prs.slides.add_slide(blank)
add_slide_header(s, "The integration gap",
                 kicker_text="Each adaptive technique is mature — but no one has composed all four for programming.")

# Four technique cards
techniques = [
    ("BKT",  "Bayesian Knowledge Tracing", "Corbett & Anderson, 1995"),
    ("Elo",  "Dual rating + ZPD",          "Pelánek, 2016"),
    ("MAB",  "Thompson Sampling",          "Chapelle & Li, 2011"),
    ("FSRS", "Spaced Repetition",          "Ye et al., 2022"),
]
card_w = Inches(2.6)
card_h = Inches(2.4)
gap    = Inches(0.25)
total_w = card_w * 4 + gap * 3
left0 = (SLIDE_W - total_w) // 2
top0  = Inches(2.2)

for i, (acron, full, cite) in enumerate(techniques):
    x = left0 + (card_w + gap) * i
    add_rect(s, x, top0, card_w, card_h, LIGHT, MUTED)
    add_rect(s, x, top0, card_w, Inches(0.08), ORANGE)
    add_textbox(s, x, top0 + Inches(0.3), card_w, Inches(0.7),
                acron, size=36, bold=True, color=NAVY,
                align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_textbox(s, x, top0 + Inches(1.05), card_w, Inches(0.6),
                full, size=14, color=SLATE,
                align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_textbox(s, x, top0 + Inches(1.7), card_w, Inches(0.5),
                cite, size=11, italic=True, color=MUTED_TEXT,
                align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# Bottom message
add_paragraphs(s, Inches(0.6), Inches(5.0), Inches(12.1), Inches(2.0),
               [
                {"text": "Studied alone or in pairs.", "size": 18, "bold": True, "color": NAVY},
                {"text": " ", "size": 8},
                {"text": "Commercial platforms (LeetCode, HackerRank, Codeforces) have huge problem libraries —",
                 "size": 14, "color": SLATE},
                {"text": "but rely on static difficulty tags and offer no closed loop from learner outcome back to problem selection.",
                 "size": 14, "color": SLATE},
                {"text": " ", "size": 8},
                {"text": "→ This paper closes that loop, and integrates all four under a shared knowledge graph.",
                 "size": 16, "bold": True, "color": ORANGE},
               ], align=PP_ALIGN.CENTER)
add_footer(s, 3, TOTAL)


# =======================================================================
# Slide 4 — Five-layer architecture (Figure 1)
# =======================================================================
s = prs.slides.add_slide(blank)
add_slide_header(s, "A five-layer adaptive engine on a shared knowledge graph",
                 kicker_text="Knowledge graph: 28 programming concepts, ~45 prerequisite edges, 5 difficulty tiers, 7 topic clusters.")

fit_image(s, VIS / "ch3-system-architecture-diagram.png",
          Inches(0.6), Inches(1.9), Inches(8.0), Inches(5.0))

# Layer legend on right
add_paragraphs(s, Inches(8.9), Inches(1.9), Inches(4.0), Inches(5.0),
               [
                {"text": "Layer 1 — BKT", "size": 16, "bold": True, "color": NAVY},
                {"text": "per-concept mastery posterior", "size": 12, "color": SLATE},
                {"text": " ", "size": 6},
                {"text": "Layer 2 — Dynamic Elo", "size": 16, "bold": True, "color": NAVY},
                {"text": "difficulty calibration + ZPD", "size": 12, "color": SLATE},
                {"text": " ", "size": 6},
                {"text": "Layer 3 — Hierarchical MAB", "size": 16, "bold": True, "color": NAVY},
                {"text": "concept → problem selection", "size": 12, "color": SLATE},
                {"text": " ", "size": 6},
                {"text": "Layer 4 — FSRS", "size": 16, "bold": True, "color": NAVY},
                {"text": "review scheduling", "size": 12, "color": SLATE},
                {"text": " ", "size": 6},
                {"text": "Layer 5 — LLM hints", "size": 16, "bold": True, "color": SLATE,
                 "italic": True},
                {"text": "optional, off in evaluation", "size": 12, "italic": True, "color": MUTED_TEXT},
               ])
add_footer(s, 4, TOTAL)


# =======================================================================
# Slide 5 — Layer 1 BKT
# =======================================================================
s = prs.slides.add_slide(blank)
add_slide_header(s, "Layer 1 — Bayesian Knowledge Tracing",
                 kicker_text="Per-concept mastery posterior, interpretable, cold-start friendly.")

# left: the four parameters + design choice
add_paragraphs(s, Inches(0.6), Inches(1.9), Inches(6.0), Inches(5.0),
               [
                {"text": "Four-parameter HMM, per concept", "size": 18, "bold": True, "color": NAVY},
                {"text": " ", "size": 8},
                {"text": "P(L₀)  prior knowledge", "size": 14, "color": SLATE, "mono": True},
                {"text": "P(T)   transition (learning) probability", "size": 14, "color": SLATE, "mono": True},
                {"text": "P(G)   guess  •  P(S)  slip", "size": 14, "color": SLATE, "mono": True},
                {"text": " ", "size": 8},
                {"text": "Mastered when posterior P(L) ≥ θₘ = 0.85.",
                 "size": 14, "italic": True, "color": NAVY},
                {"text": " ", "size": 16},
                {"text": "Design choice — tiered priors, not textbook BKT",
                 "size": 18, "bold": True, "color": ORANGE},
                {"text": " ", "size": 4},
                {"text": "Each of the 5 difficulty tiers gets its own (P(L₀), P(T), P(G), P(S)).",
                 "size": 13, "color": SLATE},
                {"text": "→ Calibrated cold-start across the curriculum, not one prior fits all.",
                 "size": 13, "color": SLATE},
                {"text": " ", "size": 8},
                {"text": "Why BKT, not Deep Knowledge Tracing?",
                 "size": 14, "bold": True, "color": NAVY},
                {"text": "Interpretable. Data-efficient (~hundreds of learners).",
                 "size": 12, "color": SLATE},
                {"text": "Posterior consumed by the bandit downstream — calibration matters more than raw accuracy.",
                 "size": 12, "color": SLATE},
               ])

# right: ch4-bkt-params-table.png OR state transition
fit_image(s, VIS / "ch4-bkt-params-table.png",
          Inches(7.0), Inches(1.9), Inches(5.8), Inches(5.0))
add_footer(s, 5, TOTAL)


# =======================================================================
# Slide 6 — Layer 2 Elo + ZPD
# =======================================================================
s = prs.slides.add_slide(blank)
add_slide_header(s, "Layer 2 — Dynamic Elo + Zone of Proximal Development",
                 kicker_text="Difficulty calibration that operationalises Bjork’s desirable difficulty.")

# Left column — dual Elo + dynamic K
add_paragraphs(s, Inches(0.6), Inches(1.9), Inches(6.0), Inches(5.0),
               [
                {"text": "Dual ratings", "size": 18, "bold": True, "color": NAVY},
                {"text": "Each learner rated. Each problem rated.", "size": 14, "color": SLATE},
                {"text": "Initial: learner = 1200; problem = 1000 / 1200 / 1400 (E / M / H), clamped to [400, 2800].",
                 "size": 13, "color": SLATE, "mono": True},
                {"text": " ", "size": 10},
                {"text": "Dynamic K-factor   K ∈ [10, 40]",
                 "size": 18, "bold": True, "color": NAVY},
                {"text": "K shrinks for stable learners → higher K when struggling, lower K when steady.",
                 "size": 13, "color": SLATE},
                {"text": "Computed from an exponentially weighted residual trend over the last 10 submissions.",
                 "size": 13, "color": SLATE},
                {"text": " ", "size": 10},
                {"text": "ZPD filter   δ ∈ [50, 250]",
                 "size": 18, "bold": True, "color": ORANGE},
                {"text": "Keep only problems whose Elo is in [student_elo + 50, student_elo + 250].",
                 "size": 13, "color": SLATE, "mono": True},
                {"text": "≈ 36–64% predicted success — “hard, but not too hard”.",
                 "size": 13, "italic": True, "color": NAVY},
                {"text": " ", "size": 10},
                {"text": "→ This filtered candidate pool is what Layer 3 picks from.",
                 "size": 14, "bold": True, "color": NAVY},
               ])

# Right — visual: ZPD band sketch as shapes
right_x = Inches(7.0)
add_rect(s, right_x, Inches(2.0), Inches(5.8), Inches(5.0), LIGHT, MUTED)
add_textbox(s, right_x, Inches(2.15), Inches(5.8), Inches(0.4),
            "Predicted success vs. learner rating",
            size=13, bold=True, color=NAVY, align=PP_ALIGN.CENTER)

# number-line representation
nl_y  = Inches(4.7)
nl_x0 = right_x + Inches(0.4)
nl_x1 = right_x + Inches(5.4)
nl_w  = nl_x1 - nl_x0
add_rect(s, nl_x0, nl_y, nl_w, Inches(0.04), SLATE)
# tick marks
ticks = [(0.0, "−250"), (0.25, "−50"), (0.5, "0"), (0.75, "+50"), (1.0, "+250")]
# but we want δ band, so put learner at center; use simpler band
# ZPD band from 0.5+50 to 0.5+250 (i.e. right half of axis)
band_left  = nl_x0 + int(nl_w * 0.55)
band_right = nl_x0 + int(nl_w * 0.95)
add_rect(s, band_left, nl_y - Inches(0.5), band_right - band_left, Inches(1.0),
         RGBColor(0xFF, 0xE5, 0xD9), ORANGE)
add_textbox(s, band_left, nl_y - Inches(0.85), band_right - band_left, Inches(0.3),
            "ZPD band (δ ∈ [50, 250])",
            size=11, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)

# learner rating marker
learner_x = nl_x0 + int(nl_w * 0.5)
add_rect(s, learner_x - Inches(0.04), nl_y - Inches(0.25), Inches(0.08), Inches(0.55), NAVY)
add_textbox(s, learner_x - Inches(0.7), nl_y + Inches(0.35), Inches(1.4), Inches(0.3),
            "Learner Elo",
            size=11, bold=True, color=NAVY, align=PP_ALIGN.CENTER)

# axis labels
add_textbox(s, nl_x0 - Inches(0.3), nl_y + Inches(0.05), Inches(0.6), Inches(0.3),
            "−250", size=10, color=SLATE, align=PP_ALIGN.CENTER)
add_textbox(s, nl_x1 - Inches(0.3), nl_y + Inches(0.05), Inches(0.6), Inches(0.3),
            "+250", size=10, color=SLATE, align=PP_ALIGN.CENTER)

# success rate annotation
add_textbox(s, right_x + Inches(0.3), Inches(5.6), Inches(5.4), Inches(0.4),
            "Inside the band: predicted success ≈ 36–64%",
            size=13, italic=True, color=NAVY, align=PP_ALIGN.CENTER)
add_textbox(s, right_x + Inches(0.3), Inches(6.0), Inches(5.4), Inches(0.4),
            "(Bjork’s desirable difficulty, formalised by Pelánek 2016)",
            size=11, italic=True, color=MUTED_TEXT, align=PP_ALIGN.CENTER)
add_footer(s, 6, TOTAL)


# =======================================================================
# Slide 7 — Layer 3 Hierarchical MAB
# =======================================================================
s = prs.slides.add_slide(blank)
add_slide_header(s, "Layer 3 — Hierarchical MAB with prerequisite gating",
                 kicker_text="Two-level Thompson Sampling: outer arm gated by BKT mastery; inner arm by Layer 2’s ZPD.")

# Left — mab-decision-flow image
fit_image(s, VIS / "ch4-mab-decision-flow.png",
          Inches(0.6), Inches(1.9), Inches(6.5), Inches(5.0))

# Right — explanation
add_paragraphs(s, Inches(7.4), Inches(1.9), Inches(5.4), Inches(5.0),
               [
                {"text": "Two-level Thompson Sampling", "size": 18, "bold": True, "color": NAVY},
                {"text": "Outer arm = next concept to practise.", "size": 13, "color": SLATE},
                {"text": "Inner arm = next problem within that concept.", "size": 13, "color": SLATE},
                {"text": "Each arm: Beta(α, β) posterior, updated on every reward.",
                 "size": 13, "color": SLATE, "mono": True},
                {"text": " ", "size": 10},
                {"text": "Prerequisite gate", "size": 18, "bold": True, "color": ORANGE},
                {"text": "A concept becomes an arm only when",
                 "size": 13, "color": SLATE},
                {"text": "every prerequisite has BKT mastery ≥ θₘ = 0.85.",
                 "size": 13, "color": NAVY, "mono": True},
                {"text": "Inner level then filtered by Layer 2’s ZPD band.",
                 "size": 13, "color": SLATE},
                {"text": " ", "size": 10},
                {"text": "Reward = scalar in [0, 1]",
                 "size": 18, "bold": True, "color": NAVY},
                {"text": "0.5 · learning gain   (BKT posterior delta)",
                 "size": 13, "color": SLATE, "mono": True},
                {"text": "0.3 · correctness   (attempt-aware)",
                 "size": 13, "color": SLATE, "mono": True},
                {"text": "0.2 · efficiency   (capped at 300 s)",
                 "size": 13, "color": SLATE, "mono": True},
                {"text": "Heuristic weights — re-estimation from pilot traces is named future work.",
                 "size": 11, "italic": True, "color": MUTED_TEXT},
               ])
add_footer(s, 7, TOTAL)


# =======================================================================
# Slide 8 — Layer 4 FSRS — the novelty slide
# =======================================================================
s = prs.slides.add_slide(blank)
add_slide_header(s, "Layer 4 — FSRS for programming retention",
                 kicker_text="Novel: first reported application of FSRS to programming, via a code-submission-to-rating mapping.")

# Left — retrievability curve image
fit_image(s, VIS / "ch4-fsrs-retrievability-curve.png",
          Inches(0.6), Inches(1.9), Inches(5.8), Inches(5.0))

# Right — the mapping shown verbatim, large
add_textbox(s, Inches(6.7), Inches(1.85), Inches(6.3), Inches(0.5),
            "Code submission → FSRS rating",
            size=18, bold=True, color=NAVY)
add_textbox(s, Inches(6.7), Inches(2.3), Inches(6.3), Inches(0.4),
            "fsrs_service.py · submission_to_fsrs_rating()",
            size=11, italic=True, color=MUTED_TEXT, font=MONO)

# code-style block
code_left = Inches(6.7); code_top = Inches(2.8)
code_w = Inches(6.3); code_h = Inches(3.6)
add_rect(s, code_left, code_top, code_w, code_h, RGBColor(0x1A, 0x20, 0x2C))

code_lines = [
    ("if not is_correct:", WHITE),
    ("    return 1   # Again", ORANGE),
    ("if attempt_number == 1:", WHITE),
    ("    if time_spent < 120:", WHITE),
    ("        return 4   # Easy", ORANGE),
    ("    elif time_spent < 300:", WHITE),
    ("        return 3   # Good", ORANGE),
    ("    else:", WHITE),
    ("        return 2   # Hard", ORANGE),
    ("else:", WHITE),
    ("    return 2   # Hard", ORANGE),
]

tb = s.shapes.add_textbox(code_left + Inches(0.2), code_top + Inches(0.2),
                          code_w - Inches(0.4), code_h - Inches(0.4))
tf = tb.text_frame; tf.word_wrap = True
tf.margin_left = Inches(0); tf.margin_right = Inches(0)
tf.margin_top = Inches(0); tf.margin_bottom = Inches(0)
for i, (line, col) in enumerate(code_lines):
    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
    p.line_spacing = 1.1
    r = p.add_run(); r.text = line
    r.font.name = MONO; r.font.size = Pt(15)
    r.font.color.rgb = col

add_textbox(s, Inches(6.7), Inches(6.55), Inches(6.3), Inches(0.45),
            "Review fires when retrievability R(t) drops below 0.9.",
            size=13, italic=True, color=NAVY)
add_footer(s, 8, TOTAL)


# =======================================================================
# Slide 9 — The closed loop (Figure 2)
# =======================================================================
s = prs.slides.add_slide(blank)
add_slide_header(s, "The closed loop — every code submission",
                 kicker_text="One concrete submission, four parallel updates, sub-500-ms recommendation.")

fit_image(s, VIS / "ch4-adaptive-engine-sequence.png",
          Inches(0.6), Inches(1.9), Inches(8.2), Inches(5.2))

add_paragraphs(s, Inches(9.1), Inches(1.9), Inches(3.8), Inches(5.2),
               [
                {"text": "1. Submit", "size": 16, "bold": True, "color": NAVY},
                {"text": "Python code, sandboxed.", "size": 12, "color": SLATE},
                {"text": "256 MB · 5 s · no network · unprivileged.",
                 "size": 11, "italic": True, "color": MUTED_TEXT, "mono": True},
                {"text": " ", "size": 10},
                {"text": "2. Verdict", "size": 16, "bold": True, "color": NAVY},
                {"text": "(correctness, attempts, time)", "size": 12, "color": SLATE},
                {"text": " ", "size": 10},
                {"text": "3. asyncio.gather(…)", "size": 16, "bold": True, "color": ORANGE, "mono": True},
                {"text": "BKT updates posterior",   "size": 12, "color": SLATE},
                {"text": "Elo updates both ratings", "size": 12, "color": SLATE},
                {"text": "FSRS rewrites due date",   "size": 12, "color": SLATE},
                {"text": "MAB re-ranks candidates",  "size": 12, "color": SLATE},
                {"text": " ", "size": 10},
                {"text": "4. Cache invalidated", "size": 16, "bold": True, "color": NAVY},
                {"text": "Next request gets fresh state.", "size": 12, "color": SLATE},
                {"text": " ", "size": 10},
                {"text": "→ The learner model is never stale.",
                 "size": 14, "bold": True, "color": NAVY},
               ])
add_footer(s, 9, TOTAL)


# =======================================================================
# Slide 10 — The artifact today
# =======================================================================
s = prs.slides.add_slide(blank)
add_slide_header(s, "The artifact today",
                 kicker_text="Built. Deployed. Tested. Open-source.")

# left: tech stack table image
fit_image(s, VIS / "ch4-tech-stack-table.png",
          Inches(0.6), Inches(1.9), Inches(7.4), Inches(5.0))

# right: stat block
right_x = Inches(8.3)
add_rect(s, right_x, Inches(1.9), Inches(4.5), Inches(5.0), LIGHT, MUTED)
add_rect(s, right_x, Inches(1.9), Inches(4.5), Inches(0.08), ORANGE)

stats = [
    ("~15 k", "lines of code (Python + TS)"),
    ("28", "concepts · 45 prerequisite edges"),
    ("170", "curated problems"),
    ("< 500 ms", "p95 recommendation latency"),
    ("100", "concurrent users (NFR target)"),
    ("1", "command Docker deployment"),
]
top = Inches(2.1)
row_h = Inches(0.78)
for i, (num, label) in enumerate(stats):
    y = top + row_h * i
    add_textbox(s, right_x + Inches(0.25), y, Inches(1.6), row_h,
                num, size=22, bold=True, color=ORANGE,
                anchor=MSO_ANCHOR.MIDDLE)
    add_textbox(s, right_x + Inches(1.95), y, Inches(2.4), row_h,
                label, size=12, color=NAVY,
                anchor=MSO_ANCHOR.MIDDLE)
add_footer(s, 10, TOTAL)


# =======================================================================
# Slide 11 — Pre-registered pilot (Figure 3)
# =======================================================================
s = prs.slides.add_slide(blank)
add_slide_header(s, "What is *not* in this paper — the pre-registered pilot",
                 kicker_text="Designed, IRB-cleared, pre-registered. Empirical results in a follow-up.")

fit_image(s, VIS / "ch5-experiment-timeline.png",
          Inches(0.6), Inches(1.9), Inches(8.4), Inches(5.0))

add_paragraphs(s, Inches(9.3), Inches(1.9), Inches(3.6), Inches(5.0),
               [
                {"text": "Design", "size": 16, "bold": True, "color": NAVY},
                {"text": "Between-subjects, pre/post test.", "size": 13, "color": SLATE},
                {"text": "Control = same UI, non-adaptive recommendations.",
                 "size": 13, "color": SLATE},
                {"text": " ", "size": 10},
                {"text": "Cohort", "size": 16, "bold": True, "color": NAVY},
                {"text": "n = 40–60 undergraduates", "size": 13, "color": SLATE},
                {"text": "Hanoi University, IRB-cleared.", "size": 13, "color": SLATE},
                {"text": " ", "size": 10},
                {"text": "Schedule", "size": 16, "bold": True, "color": NAVY},
                {"text": "4 weeks intervention + Week 8 retention.",
                 "size": 13, "color": SLATE},
                {"text": " ", "size": 10},
                {"text": "RQ1 (primary)", "size": 16, "bold": True, "color": ORANGE},
                {"text": "BKT + Elo predictive validity.", "size": 13, "color": SLATE},
                {"text": "Target AUC ≥ 0.70.", "size": 13, "color": NAVY, "bold": True, "mono": True},
                {"text": " ", "size": 10},
                {"text": "RQ2 / RQ3 = supporting:", "size": 12, "italic": True, "color": MUTED_TEXT},
                {"text": "acceptance rate, convergence, learning gain.",
                 "size": 12, "italic": True, "color": MUTED_TEXT},
               ])
add_footer(s, 11, TOTAL)


# =======================================================================
# Slide 12 — Contributions, recapped
# =======================================================================
s = prs.slides.add_slide(blank)
add_slide_header(s, "Contributions, recapped")

contribs = [
    ("C1", "Integrated five-layer adaptive platform",
     "BKT + Elo + Hierarchical MAB + FSRS, unified by a knowledge graph of 28 programming concepts. "
     "The prerequisite-constrained bandit (BKT-mastery-gated arms) and the code-submission-to-FSRS-rating "
     "mapping are internal technical innovations that make this integration work, "
     "not separate claims. Deployed and open-sourced."),
    ("C2", "Pre-registered pilot evaluation protocol",
     "Between-subjects classroom study, 4-week intervention + Week-8 retention follow-up, "
     "n = 40–60 Hanoi University undergraduates. IRB-cleared. Primary RQ: BKT/Elo predictive validity, AUC ≥ 0.70. "
     "Empirical results to be reported in a follow-up paper."),
]

top0 = Inches(2.0)
row_h = Inches(2.1)
for i, (tag, head, body) in enumerate(contribs):
    y = top0 + row_h * i
    add_rect(s, Inches(0.6), y + Inches(0.1), Inches(1.0), Inches(1.6), NAVY)
    add_textbox(s, Inches(0.6), y + Inches(0.1), Inches(1.0), Inches(1.6),
                tag, size=28, bold=True, color=WHITE,
                align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_textbox(s, Inches(1.85), y + Inches(0.05), Inches(11.0), Inches(0.5),
                head, size=20, bold=True, color=NAVY)
    add_textbox(s, Inches(1.85), y + Inches(0.6), Inches(11.0), Inches(1.4),
                body, size=14, color=SLATE)

# closing artifact-vs-plan caveat
add_paragraphs(s, Inches(0.6), Inches(6.4), Inches(12.2), Inches(0.7),
               [
                {"text": "C1 is implemented and demonstrated technically. ",
                 "size": 14, "color": NAVY},
                {"text": "C2 is specified, IRB-reviewed, and pre-registered — but not yet executed.",
                 "size": 14, "italic": True, "color": ORANGE},
               ], align=PP_ALIGN.CENTER)
add_footer(s, 12, TOTAL)


# =======================================================================
# Slide 13 — Closing + Q&A
# =======================================================================
s = prs.slides.add_slide(blank)
add_rect(s, 0, 0, Inches(0.45), SLIDE_H, NAVY)

add_textbox(s, Inches(0.8), Inches(1.0), Inches(11.5), Inches(0.5),
            "Thank you.",
            size=20, italic=True, color=ORANGE)

add_textbox(s, Inches(0.8), Inches(2.0), Inches(11.5), Inches(2.8),
            "By integrating four adaptive techniques\nthat have, until now, been studied in isolation,\nthis work offers a working architectural step\ntoward individualised programming education at scale.",
            size=28, bold=True, color=NAVY)

# divider
add_rect(s, Inches(0.8), Inches(4.9), Inches(0.9), Inches(0.08), ORANGE)

add_textbox(s, Inches(0.8), Inches(5.05), Inches(11.5), Inches(0.5),
            "Questions?",
            size=24, bold=True, color=NAVY)

add_textbox(s, Inches(0.8), Inches(5.9), Inches(11.5), Inches(0.4),
            "Nguyễn Tuấn Dương · Class 1C22 · Faculty of IT · Hanoi University",
            size=13, color=SLATE)
add_textbox(s, Inches(0.8), Inches(6.3), Inches(11.5), Inches(0.4),
            "Email: ntduongvbhp@gmail.com",
            size=13, color=SLATE)
add_textbox(s, Inches(0.8), Inches(6.7), Inches(11.5), Inches(0.4),
            "Advisor: M.Sc. Bùi Quốc Khánh",
            size=13, italic=True, color=SLATE)


# ---------- save ----------
OUT.parent.mkdir(parents=True, exist_ok=True)
prs.save(OUT)
print(f"OK - wrote {OUT.relative_to(ROOT)}  ({OUT.stat().st_size//1024} KB, {len(prs.slides)} slides)")
