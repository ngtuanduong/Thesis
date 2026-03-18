"""
Publish Chapter 1 (Introduction) to a Google Doc with professional academic formatting.

Formatting standards:
- Body text: Times New Roman, 12pt, Regular, justified, 1.27cm first-line indent
- Heading 1: Times New Roman, 14pt, Bold, ALL CAPS
- Heading 2: Times New Roman, 13pt, Bold
- Heading 3: Times New Roman, 12pt, Bold, Italic
- Line spacing: 1.5
- Paragraph spacing: 6pt after
- Tables: Times New Roman 12pt, header row bold
- Captions: Times New Roman 12pt, italic, centered

Visuals from VISUAL-GUIDE.md are inserted as inline images from catbox.moe URLs.
"""

import re
import sys
import time
from dataclasses import dataclass, field
from enum import Enum, auto

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

CREDENTIALS_PATH = '/Users/avada/WebstormProjects/Thesis/infra-inkwell-465003-f2-369235afe5ac.json'
CHAPTER_PATH = '/Users/avada/WebstormProjects/Thesis/documents/thesis-chapters/chapter1-introduction.md'
DEFAULT_DOC_ID = '1Q1mihSftbOtxuPTitDmcdjE7Av-EHxyjgZAfqw3Gfok'

# ---------------------------------------------------------------------------
# Humanized text replacements (from QuillBot AI Humanizer)
# Keys are the first 60 chars of the original paragraph text.
# Values are the humanized replacement text.
# ---------------------------------------------------------------------------
HUMANIZED_PARAGRAPHS = {
    # Section 1.1 Paragraph 1 (two chunks combined)
    "Programming has become a foundational competency in higher education worldwide":
        "Over the past 20 years, enrollment in introductory computer science courses has steadily increased, making programming a fundamental skill in higher education across the globe. However, despite this increase in demand, programming education still faces a long-standing and well-documented crisis: high failure and dropout rates that are significantly higher than those of the majority of other undergraduate fields. The average failure rate in introductory programming courses is between 30% and 40% worldwide, according to a thorough systematic literature review by Luxton-Reilly et al. [1]. This figure has remained remarkably stable over several decades of pedagogical experimentation. The diversity of student backgrounds is one of the main obstacles, according to Robins et al.'s [2] groundbreaking review of learning and teaching programming. While some students come with years of self-taught coding experience, others encounter their first line of code on the first day of class.",

    # Section 1.1 Paragraph 2
    "This heterogeneity creates a fundamental tension in traditional lecture-based":
        "Traditional lecture-based instruction is fundamentally tense due to this heterogeneity. The instructor in a typical 50 to 100 student university programming class is required to present the material at a single pace and difficulty level. While they wait for their peers to catch up, students who already have fundamental skills become disengaged. On the other hand, students who don't have any prior exposure gradually lag behind because they can't bridge the gap between understanding syntax and acquiring the computational thinking needed to solve problems on their own. Programming, unlike many academic subjects, is at its core a skill that calls for deliberate, individualized practice [3]. No amount of well-designed lectures can replace the iterative cycle of writing code, running into errors, debugging, and refining solutions.",

    # Section 1.1 Paragraph 3
    "The problem is compounded by the resource constraints that instructors face":
        "The resource constraints that instructors face make the problem even worse. Giving personalized feedback on student code, spotting misconceptions, recommending targeted practice problems, and tracking individual progress across multiple programming concepts takes time and effort that grow linearly with class size. In large sections, meaningful one-on-one instruction becomes practically impossible. Grading coding assignments is time-consuming by itself, and when feedback is delayed, its pedagogical value drops because students have usually moved on to new topics by the time they get comments on prior work.",

    # Section 1.1 Paragraph 4
    "Within the Vietnamese university context specifically, these challenges are no less pressing":
        "Within the Vietnamese university context, these challenges are just as pressing. Programming courses at Vietnamese institutions deal with the same variety in student preparation, the same constraints of one-size-fits-all teaching, and additional hurdles including limited access to advanced educational technology platforms and a lack of adaptive learning tools built for local curricula [4]. A worldwide systematic review by Watson and Li [5] found a mean failure rate of 32.3% across 161 courses in 15 countries, showing that this is not just a local issue but a global challenge that Vietnamese institutions share. The gap between the rising demand for software engineering graduates and the effectiveness of current programming pedagogy is both an educational and an economic concern.",

    # Section 1.1 Paragraph 5
    "In summary, the core problem this thesis addresses is the mismatch":
        "In short, the core problem this thesis takes on is the mismatch between the individualized, practice-heavy nature of programming skill development and the uniform, resource-limited reality of university instruction. Students need personalized learning paths, appropriately challenging practice problems, timely feedback, and systematic review of concepts they have already learned, yet current educational practices and platforms provide none of these at scale.",

    # Section 1.2.1 Paragraph 1
    "Adaptive learning --- the practice of adjusting instructional content":
        "Adaptive learning, the practice of tailoring instructional content, pace, and methods based on individual learner traits and performance, has shown significant effectiveness across multiple educational domains [6], [7]. The core idea is that learning works best when instruction matches the learner's current knowledge state, cognitive ability, and learning trajectory.",

    # Section 1.2.1 Paragraph 2
    "Research spanning several decades has validated this premise":
        "Research going back several decades has confirmed this premise. Early Intelligent Tutoring Systems like the Cognitive Tutor series showed 50 to 100% gains in problem-solving skills [3], [8], while modern platforms such as ALEKS [9] and Duolingo [10] have demonstrated that machine learning-driven adaptation can work effectively at scale. A thorough review of these systems and how they have evolved is provided in Chapter 2.",

    # Section 1.2.1 Paragraph 3
    "These success stories motivate the application of adaptive learning to programming":
        "These success stories point toward applying adaptive learning to programming education, a field whose properties make it especially well-suited to data-driven personalization.",

    # Section 1.2.2 Paragraph 1
    "Programming education possesses several characteristics that distinguish":
        "Programming education has several traits that set it apart from other fields and make it a strong candidate for adaptive learning systems:",

    # Section 1.2.2 Conclusion
    "These properties mean that an adaptive system for programming can leverage":
        "These properties mean that an adaptive system for programming can draw on unusually rich data to model student knowledge with high accuracy, recommend problems at precisely calibrated difficulty levels, and deliver targeted feedback, capabilities that are difficult or impossible to achieve through manual instruction alone.",

    # Section 1.2.3 Paragraph 1
    "Despite the strong case for adaptive learning in programming, existing online coding platforms fail":
        "Despite the compelling case for adaptive learning in programming, existing online coding platforms fall short of delivering comprehensive adaptation. Platforms like LeetCode, HackerRank, and Codeforces have reached remarkable scale with millions of users, but their pedagogical design remains fundamentally static:",

    # Section 1.2.3 Paragraph 2
    "A systematic comparison reveals that no existing platform":
        "A systematic comparison shows that no existing platform, whether academic or commercial, brings together all the components that learning science says are needed for effective personalized instruction: modeling what the student knows (knowledge tracing), calibrating how hard each problem is for each individual (difficulty calibration), picking which problem to recommend next to maximize learning (intelligent selection), scheduling when to review previously learned concepts to prevent forgetting (spaced repetition), and offering contextual help when the student is stuck (feedback generation) [see Table 1.1]. The table covers both programming-focused platforms (LeetCode through CodeSignal) and adaptive learning platforms from other fields (Duolingo through Knewton Alta); the research gap this thesis targets sits precisely at their intersection, bringing the adaptive sophistication of the latter category into the programming education domain.",

    # Section 1.2.3 Paragraph 3
    "The platforms in Table 1.1 were selected based on two criteria":
        "The platforms in Table 1.1 were chosen based on two criteria: (1) commercial platforms with over one million active users that are widely used for programming practice or adaptive learning, and (2) well-known academic systems from the Intelligent Tutoring Systems and Adaptive Learning literature. The comparison focuses on whether each platform integrates the six adaptive components identified above.",

    # Section 1.2.3 Paragraph 4
    "Academic research, similarly, has tended to study these adaptive components in isolation":
        "Academic research has also tended to study these adaptive components separately. Knowledge tracing papers measure prediction accuracy but don't build recommendation systems around their models. Multi-Armed Bandit papers for education assume fixed difficulty models rather than adaptive ones. The FSRS algorithm was created for flashcard-based memorization (vocabulary, facts) and has not yet been applied to programming skill retention. Each line of work addresses one part of the problem but leaves the integration challenge unresolved.",

    # Section 1.2.3 Paragraph 5
    "This thesis aims to address this integration gap":
        "This thesis sets out to address this integration gap by proposing and evaluating a unified adaptive platform that brings together all five components into a coherent, closed-loop system.",

    # Section 1.3 Paragraph 1
    "The primary aim of this thesis is to design, implement, and evaluate":
        "The primary goal of this thesis is to design, build, and evaluate an adaptive learning platform for university programming courses that brings together multiple complementary adaptive techniques into a unified, closed-loop system. The specific objectives are as follows:",

    # Section 1.4 Intro
    "This thesis addresses four research questions":
        "This thesis tackles four research questions, one primary and three secondary. For comparative questions (RQ2, RQ3), corresponding hypotheses are stated and will be tested at the alpha = 0.05 significance level.",

    # Section 1.5 Paragraph 1
    "This thesis proposes an Adaptive Learning Platform for University Programming Courses":
        "This thesis puts forward an Adaptive Learning Platform for University Programming Courses built on a five-layer adaptive engine, unified through a knowledge graph of programming concepts. The system works as a closed loop: student interactions produce data that updates the learner model, which in turn shapes subsequent recommendations, creating a continuously evolving personalized learning experience.",

    # Section 1.5.2 Intro
    "The system operates through a continuous feedback cycle":
        "The system runs through a continuous feedback cycle:",

    # Section 1.5.2 Conclusion
    "This closed-loop design ensures that the learning experience evolves continuously":
        "This closed-loop design means that the learning experience evolves continuously with the student's progress, keeping challenge levels in the right range and preventing the stagnation that happens when recommendations are based on static profiles.",

    # Section 1.7 Intro
    "This thesis makes the following contributions to the fields":
        "This thesis makes the following contributions to the fields of educational technology and computer science education:",

    # Section 1.8 Intro
    "The remainder of this thesis is organized as follows":
        "The rest of this thesis is organized as follows:",
}


def humanize_paragraph(text: str) -> str:
    """Look up humanized replacement for a paragraph, or return original."""
    for key, replacement in HUMANIZED_PARAGRAPHS.items():
        if text.strip().startswith(key):
            return replacement
    return text


# Chapter 1 visuals from VISUAL-GUIDE.md
VISUALS = {
    'table_1_1': {
        'url': 'https://files.catbox.moe/5j02nc.png',
        'caption': 'Table 1.1. Comparison of adaptive capabilities across existing platforms and this thesis.',
        'width': 468,
        'height': 280,
    },
    'figure_1_1': {
        'url': 'https://files.catbox.moe/iiyquw.png',
        'caption': 'Figure 1.1. Research gap diagram showing the intersection between programming platforms and adaptive learning platforms.',
        'width': 468,
        'height': 350,
    },
    'figure_1_2': {
        'url': 'https://files.catbox.moe/eygpcs.png',
        'caption': 'Figure 1.2. Closed-loop adaptive workflow showing the continuous feedback cycle.',
        'width': 468,
        'height': 320,
    },
    'figure_1_3': {
        'url': 'https://files.catbox.moe/uq1e9d.png',
        'caption': 'Figure 1.3. Five-layer architecture overview of the adaptive learning platform.',
        'width': 468,
        'height': 380,
    },
    'figure_1_4': {
        'url': 'https://files.catbox.moe/ve758p.png',
        'caption': 'Figure 1.4. Thesis structure roadmap showing chapter flow, contributions, and research questions.',
        'width': 468,
        'height': 350,
    },
}


# ---------------------------------------------------------------------------
# Markdown Parser (enhanced from existing script)
# ---------------------------------------------------------------------------

class BlockType(Enum):
    HEADING = auto()
    PARAGRAPH = auto()
    TABLE = auto()
    CODE_BLOCK = auto()
    ORDERED_LIST = auto()
    UNORDERED_LIST = auto()
    HORIZONTAL_RULE = auto()
    MATH_BLOCK = auto()
    FOOTNOTE = auto()
    IMAGE_PLACEHOLDER = auto()
    CAPTION = auto()


@dataclass
class InlineSpan:
    text: str
    bold: bool = False
    italic: bool = False
    code: bool = False


@dataclass
class Block:
    type: BlockType
    level: int = 0
    raw_text: str = ""
    spans: list = field(default_factory=list)
    rows: list = field(default_factory=list)
    items: list = field(default_factory=list)
    language: str = ""
    visual_key: str = ""


def parse_inline(text: str) -> list:
    """Parse inline markdown formatting into spans."""
    spans = []
    i = 0
    n = len(text)

    while i < n:
        # Inline code
        if text[i] == '`' and not (i + 1 < n and text[i + 1] == '`'):
            end = text.find('`', i + 1)
            if end != -1:
                spans.append(InlineSpan(text=text[i + 1:end], code=True))
                i = end + 1
                continue

        # Bold + italic (*** or ___)
        if i + 2 < n and text[i:i + 3] in ('***', '___'):
            marker = text[i:i + 3]
            end = text.find(marker, i + 3)
            if end != -1:
                spans.append(InlineSpan(text=text[i + 3:end], bold=True, italic=True))
                i = end + 3
                continue

        # Bold (** or __)
        if i + 1 < n and text[i:i + 2] in ('**', '__'):
            marker = text[i:i + 2]
            end = text.find(marker, i + 2)
            if end != -1:
                spans.append(InlineSpan(text=text[i + 2:end], bold=True))
                i = end + 2
                continue

        # Italic (* or _)
        if text[i] in ('*', '_'):
            marker = text[i]
            if not (i + 1 < n and text[i + 1] == marker):
                end = text.find(marker, i + 1)
                if end != -1 and end > i + 1:
                    spans.append(InlineSpan(text=text[i + 1:end], italic=True))
                    i = end + 1
                    continue

        # Inline math $...$
        if text[i] == '$' and not (i + 1 < n and text[i + 1] == '$'):
            end = text.find('$', i + 1)
            if end != -1:
                spans.append(InlineSpan(text=text[i + 1:end], italic=True))
                i = end + 1
                continue

        # Plain text
        plain_end = i + 1
        while plain_end < n and text[plain_end] not in ('*', '_', '`', '$'):
            plain_end += 1
        spans.append(InlineSpan(text=text[i:plain_end]))
        i = plain_end

    return spans if spans else [InlineSpan(text="")]


def parse_markdown_chapter(content: str) -> list:
    """Parse a chapter markdown file into blocks, inserting visual placeholders."""
    lines = content.split('\n')
    blocks = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Skip empty lines
        if not line.strip():
            i += 1
            continue

        # Footnote line: \* *text*
        if line.strip().startswith('\\*'):
            footnote_text = line.strip()[2:].strip()
            # Strip surrounding italics markers if present
            if footnote_text.startswith('*') and footnote_text.endswith('*'):
                footnote_text = footnote_text[1:-1]
            blocks.append(Block(
                type=BlockType.FOOTNOTE,
                raw_text=footnote_text,
                spans=[InlineSpan(text=footnote_text, italic=True)],
            ))
            i += 1
            continue

        # Headings
        heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if heading_match:
            level = len(heading_match.group(1))
            text = heading_match.group(2).strip()
            blocks.append(Block(
                type=BlockType.HEADING,
                level=level,
                raw_text=text,
                spans=parse_inline(text),
            ))
            i += 1
            continue

        # Horizontal rule
        if re.match(r'^(-{3,}|\*{3,}|_{3,})$', line.strip()):
            blocks.append(Block(type=BlockType.HORIZONTAL_RULE))
            i += 1
            continue

        # Math block
        if line.strip().startswith('$$'):
            stripped = line.strip()
            if stripped.endswith('$$') and len(stripped) > 4:
                math_text = stripped[2:-2].strip()
                blocks.append(Block(type=BlockType.MATH_BLOCK, raw_text=math_text,
                                    spans=[InlineSpan(text=math_text, italic=True)]))
                i += 1
                continue
            math_lines = [stripped[2:]]
            i += 1
            while i < len(lines) and '$$' not in lines[i]:
                math_lines.append(lines[i])
                i += 1
            if i < len(lines):
                closing_line = lines[i].strip()
                if closing_line.endswith('$$'):
                    math_lines.append(closing_line[:-2])
                i += 1
            math_text = '\n'.join(l for l in math_lines if l.strip())
            blocks.append(Block(type=BlockType.MATH_BLOCK, raw_text=math_text,
                                spans=[InlineSpan(text=math_text, italic=True)]))
            continue

        # Code block
        if line.strip().startswith('```'):
            lang = line.strip()[3:].strip()
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1
            blocks.append(Block(type=BlockType.CODE_BLOCK, raw_text='\n'.join(code_lines), language=lang))
            continue

        # Table - check if this is the comparison table (Table 1.1)
        if line.strip().startswith('|'):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i])
                i += 1
            rows = []
            for tl in table_lines:
                cells = [c.strip() for c in tl.strip().strip('|').split('|')]
                if all(re.match(r'^:?-+:?$', c) for c in cells):
                    continue
                rows.append(cells)
            if rows:
                blocks.append(Block(type=BlockType.TABLE, rows=rows))
            continue

        # Unordered list
        if re.match(r'^(\s*[-*+]\s)', line):
            items = []
            while i < len(lines) and re.match(r'^(\s*[-*+]\s)', lines[i]):
                item_text = re.sub(r'^\s*[-*+]\s+', '', lines[i])
                items.append(parse_inline(item_text))
                i += 1
            blocks.append(Block(type=BlockType.UNORDERED_LIST, items=items))
            continue

        # Ordered list
        if re.match(r'^(\s*\d+[.)]\s)', line):
            items = []
            while i < len(lines) and re.match(r'^(\s*\d+[.)]\s)', lines[i]):
                item_text = re.sub(r'^\s*\d+[.)]\s+', '', lines[i])
                items.append(parse_inline(item_text))
                i += 1
            blocks.append(Block(type=BlockType.ORDERED_LIST, items=items))
            continue

        # Paragraph - check for caption lines like "**Table 1.1.**..."
        para_lines = []
        while i < len(lines):
            l = lines[i]
            if not l.strip():
                break
            if re.match(r'^#{1,6}\s', l):
                break
            if l.strip().startswith('```'):
                break
            if l.strip().startswith('|') and '|' in l[1:]:
                break
            if re.match(r'^(-{3,}|\*{3,}|_{3,})$', l.strip()):
                break
            if l.strip().startswith('$$'):
                break
            para_lines.append(l)
            i += 1
        if para_lines:
            text = ' '.join(para_lines)
            # Detect caption paragraphs
            if re.match(r'^\*?\*?Table \d+\.\d+\.?\*?\*?', text.strip()):
                blocks.append(Block(type=BlockType.CAPTION, raw_text=text, spans=parse_inline(text)))
            elif re.match(r'^\*?\*?Figure \d+\.\d+\.?\*?\*?', text.strip()):
                blocks.append(Block(type=BlockType.CAPTION, raw_text=text, spans=parse_inline(text)))
            else:
                blocks.append(Block(type=BlockType.PARAGRAPH, raw_text=text, spans=parse_inline(text)))

    return blocks


# ---------------------------------------------------------------------------
# Formatting constants
# ---------------------------------------------------------------------------

TIMES_NEW_ROMAN = 'Times New Roman'
COURIER_NEW = 'Courier New'

# Sizes in PT
BODY_SIZE = 12
H1_SIZE = 14
H2_SIZE = 13
H3_SIZE = 12
CODE_SIZE = 10
CAPTION_SIZE = 12
FOOTNOTE_SIZE = 10

# Spacing
LINE_SPACING = 150  # 1.5 lines (percentage)
SPACE_AFTER_PT = 6
FIRST_LINE_INDENT_PT = 36  # 1.27cm ~ 36pt


# ---------------------------------------------------------------------------
# Document builder (tracks text + formatting ranges)
# ---------------------------------------------------------------------------

@dataclass
class TextFormatRange:
    start: int
    end: int
    bold: bool = False
    italic: bool = False
    font_family: str = None
    font_size: float = None
    fg_color: dict = None
    bg_color: dict = None
    all_caps: bool = False


@dataclass
class ParaFormatRange:
    start: int
    end: int
    named_style: str = None
    alignment: str = None
    first_line_indent_pt: float = None
    indent_start_pt: float = None
    space_above_pt: float = None
    space_below_pt: float = None
    line_spacing: float = None
    keep_with_next: bool = False
    bullet_preset: str = None


@dataclass
class ImageInsert:
    """Record of an image to insert at a specific position."""
    text_offset: int  # position in the virtual text
    url: str
    width: int
    height: int
    caption: str


class ChapterBuilder:
    """Builds plain text + formatting metadata for a chapter."""

    def __init__(self):
        self.text_parts = []
        self.text_formats = []
        self.para_formats = []
        self.tables = []
        self.images = []
        self.pos = 0

    def _append(self, text):
        start = self.pos
        self.text_parts.append(text)
        self.pos += len(text)
        return start, self.pos

    def _add_spans_text(self, spans, newline=True):
        """Add spans as text, recording inline formatting."""
        block_start = self.pos
        for span in spans:
            s = self.pos
            self._append(span.text)
            e = self.pos
            fmt_fields = {}
            if span.bold:
                fmt_fields['bold'] = True
            if span.italic:
                fmt_fields['italic'] = True
            if span.code:
                fmt_fields['font_family'] = COURIER_NEW
                fmt_fields['bg_color'] = {'red': 0.94, 'green': 0.94, 'blue': 0.94}
            if fmt_fields and s < e:
                self.text_formats.append(TextFormatRange(start=s, end=e, **fmt_fields))
        if newline:
            self._append('\n')
        return block_start, self.pos

    def add_heading(self, block):
        level = block.level
        # For H1 (chapter title), convert to ALL CAPS
        if level == 1:
            # Replace span texts with uppercase
            caps_spans = []
            for span in block.spans:
                caps_spans.append(InlineSpan(
                    text=span.text.upper(),
                    bold=span.bold,
                    italic=span.italic,
                    code=span.code,
                ))
            start, end = self._add_spans_text(caps_spans)
            # Bold + font for entire heading
            self.text_formats.append(TextFormatRange(
                start=start, end=end - 1,
                bold=True, font_family=TIMES_NEW_ROMAN, font_size=H1_SIZE,
            ))
            self.para_formats.append(ParaFormatRange(
                start=start, end=end,
                named_style='HEADING_1',
                space_above_pt=24, space_below_pt=12,
                keep_with_next=True,
            ))
        elif level == 2:
            start, end = self._add_spans_text(block.spans)
            self.text_formats.append(TextFormatRange(
                start=start, end=end - 1,
                bold=True, font_family=TIMES_NEW_ROMAN, font_size=H2_SIZE,
            ))
            self.para_formats.append(ParaFormatRange(
                start=start, end=end,
                named_style='HEADING_2',
                space_above_pt=18, space_below_pt=6,
                keep_with_next=True,
            ))
        elif level == 3:
            start, end = self._add_spans_text(block.spans)
            self.text_formats.append(TextFormatRange(
                start=start, end=end - 1,
                bold=True, italic=True, font_family=TIMES_NEW_ROMAN, font_size=H3_SIZE,
            ))
            self.para_formats.append(ParaFormatRange(
                start=start, end=end,
                named_style='HEADING_3',
                space_above_pt=12, space_below_pt=6,
                keep_with_next=True,
            ))
        else:
            start, end = self._add_spans_text(block.spans)
            self.text_formats.append(TextFormatRange(
                start=start, end=end - 1,
                bold=True, font_family=TIMES_NEW_ROMAN, font_size=BODY_SIZE,
            ))
            self.para_formats.append(ParaFormatRange(
                start=start, end=end,
                named_style=f'HEADING_{min(level, 6)}',
                keep_with_next=True,
            ))

    def add_paragraph(self, block):
        start, end = self._add_spans_text(block.spans)
        # Body text gets first-line indent and justified alignment
        self.para_formats.append(ParaFormatRange(
            start=start, end=end,
            alignment='JUSTIFIED',
            first_line_indent_pt=FIRST_LINE_INDENT_PT,
            line_spacing=LINE_SPACING,
            space_below_pt=SPACE_AFTER_PT,
        ))

    def add_caption(self, block):
        """Add a caption line (centered, italic, 12pt)."""
        start, end = self._add_spans_text(block.spans)
        self.text_formats.append(TextFormatRange(
            start=start, end=end - 1,
            italic=True, font_family=TIMES_NEW_ROMAN, font_size=CAPTION_SIZE,
        ))
        self.para_formats.append(ParaFormatRange(
            start=start, end=end,
            alignment='CENTER',
            space_above_pt=6, space_below_pt=6,
        ))

    def add_footnote(self, block):
        start, end = self._add_spans_text(block.spans)
        self.text_formats.append(TextFormatRange(
            start=start, end=end - 1,
            italic=True, font_family=TIMES_NEW_ROMAN, font_size=FOOTNOTE_SIZE,
        ))
        self.para_formats.append(ParaFormatRange(
            start=start, end=end,
            space_below_pt=3,
        ))

    def add_code_block(self, block):
        start, _ = self._append(block.raw_text + '\n')
        end = self.pos
        self.text_formats.append(TextFormatRange(
            start=start, end=end,
            font_family=COURIER_NEW, font_size=CODE_SIZE,
            bg_color={'red': 0.94, 'green': 0.94, 'blue': 0.94},
        ))
        self.para_formats.append(ParaFormatRange(
            start=start, end=end,
            indent_start_pt=36,
        ))

    def add_math_block(self, block):
        start, _ = self._append(block.raw_text + '\n')
        end = self.pos
        self.text_formats.append(TextFormatRange(
            start=start, end=end,
            italic=True, font_family='Cambria Math',
        ))
        self.para_formats.append(ParaFormatRange(
            start=start, end=end,
            alignment='CENTER',
        ))

    def add_table_placeholder(self, block):
        """Record a table position; actual table inserted via API later."""
        marker = '\n'
        start = self.pos
        self._append(marker)
        self.tables.append({
            'text_offset': start,
            'rows': block.rows,
        })

    def add_list(self, block, ordered=False):
        start = self.pos
        for item_spans in block.items:
            for span in item_spans:
                s = self.pos
                self._append(span.text)
                e = self.pos
                if span.bold or span.italic or span.code:
                    fmt = {}
                    if span.bold:
                        fmt['bold'] = True
                    if span.italic:
                        fmt['italic'] = True
                    if span.code:
                        fmt['font_family'] = COURIER_NEW
                    if fmt and s < e:
                        self.text_formats.append(TextFormatRange(start=s, end=e, **fmt))
            self._append('\n')
        end = self.pos
        preset = 'NUMBERED_DECIMAL_ALPHA_ROMAN' if ordered else 'BULLET_DISC_CIRCLE_SQUARE'
        self.para_formats.append(ParaFormatRange(
            start=start, end=end,
            bullet_preset=preset,
            line_spacing=LINE_SPACING,
            space_below_pt=SPACE_AFTER_PT,
        ))

    def add_horizontal_rule(self):
        # Insert a thin gray line
        text = '___________________________________________\n'
        start, _ = self._append(text)
        end = self.pos
        self.text_formats.append(TextFormatRange(
            start=start, end=end - 1,
            fg_color={'red': 0.7, 'green': 0.7, 'blue': 0.7},
            font_size=6,
        ))
        self.para_formats.append(ParaFormatRange(
            start=start, end=end,
            alignment='CENTER',
        ))

    def add_image(self, visual_key):
        """Record an image to be inserted at the current position."""
        visual = VISUALS.get(visual_key)
        if not visual:
            print(f"  Warning: Visual '{visual_key}' not found in VISUALS map")
            return
        # The image will be inserted at this text offset
        # We add a newline placeholder for it
        start = self.pos
        self._append('\n')
        self.images.append(ImageInsert(
            text_offset=start,
            url=visual['url'],
            width=visual['width'],
            height=visual['height'],
            caption=visual['caption'],
        ))
        # Add the caption below
        cap_start = self.pos
        self._append(visual['caption'] + '\n')
        cap_end = self.pos
        self.text_formats.append(TextFormatRange(
            start=cap_start, end=cap_end - 1,
            italic=True, font_family=TIMES_NEW_ROMAN, font_size=CAPTION_SIZE,
        ))
        self.para_formats.append(ParaFormatRange(
            start=cap_start, end=cap_end,
            alignment='CENTER',
            space_above_pt=6, space_below_pt=12,
        ))

    def get_full_text(self):
        return ''.join(self.text_parts)

    def build_blocks(self, blocks):
        """Process all parsed blocks, inserting visuals at appropriate locations."""
        for idx, block in enumerate(blocks):
            if block.type == BlockType.HEADING:
                self.add_heading(block)
            elif block.type == BlockType.PARAGRAPH:
                self.add_paragraph(block)
            elif block.type == BlockType.CAPTION:
                # Check if this caption precedes a table that should be an image
                raw = block.raw_text
                if 'Table 1.1' in raw:
                    # Insert the Table 1.1 image instead of the markdown table
                    self.add_image('table_1_1')
                else:
                    self.add_caption(block)
            elif block.type == BlockType.TABLE:
                # Check if the previous block was a Table 1.1 caption
                # If so, skip the markdown table (we inserted the image)
                if idx > 0 and blocks[idx - 1].type == BlockType.CAPTION and 'Table 1.1' in blocks[idx - 1].raw_text:
                    continue  # Skip, image was already inserted
                else:
                    self.add_table_placeholder(block)
            elif block.type == BlockType.CODE_BLOCK:
                self.add_code_block(block)
            elif block.type == BlockType.MATH_BLOCK:
                self.add_math_block(block)
            elif block.type == BlockType.UNORDERED_LIST:
                self.add_list(block, ordered=False)
            elif block.type == BlockType.ORDERED_LIST:
                self.add_list(block, ordered=True)
            elif block.type == BlockType.HORIZONTAL_RULE:
                self.add_horizontal_rule()
            elif block.type == BlockType.FOOTNOTE:
                self.add_footnote(block)

        # Now insert figures at the appropriate locations based on content
        # We need to insert them at the right spots in the already-built text
        # Since we process linearly, we need to identify where figures should go
        # by scanning the text content


# ---------------------------------------------------------------------------
# Determine where to insert figures based on section content
# ---------------------------------------------------------------------------

def insert_visual_markers(blocks):
    """
    Insert IMAGE_PLACEHOLDER blocks at the right locations in the block list.
    Based on VISUAL-GUIDE.md placement guidance.
    """
    new_blocks = []
    for idx, block in enumerate(blocks):
        new_blocks.append(block)

        # Figure 1.1 (Research Gap): after paragraph mentioning Table 1.1 footnote
        # Place after the footnote that follows Table 1.1
        if block.type == BlockType.FOOTNOTE and 'This row represents' in block.raw_text:
            new_blocks.append(Block(type=BlockType.PARAGRAPH, raw_text='', spans=[InlineSpan(text='')]))
            # Add the paragraph after the table footnote, then the image
            pass

        # Figure 1.1 (Research Gap): after the paragraph about systematic comparison
        if block.type == BlockType.PARAGRAPH and 'Academic research, similarly' in block.raw_text:
            new_blocks.append(Block(type=BlockType.IMAGE_PLACEHOLDER, visual_key='figure_1_1'))

        # Figure 1.3 (Architecture): after "Architecture Overview" section content
        if block.type == BlockType.PARAGRAPH and 'coordinates all adaptive layers' in block.raw_text:
            new_blocks.append(Block(type=BlockType.IMAGE_PLACEHOLDER, visual_key='figure_1_3'))

        # Figure 1.2 (Closed-Loop): after the ordered list in section 1.5.2
        if block.type == BlockType.PARAGRAPH and 'stagnation that occurs when' in block.raw_text:
            new_blocks.append(Block(type=BlockType.IMAGE_PLACEHOLDER, visual_key='figure_1_2'))

        # Figure 1.4 (Thesis Structure): at the very end of chapter (after last paragraph of 1.8)
        if block.type == BlockType.PARAGRAPH and 'broader potential of adaptive learning' in block.raw_text:
            new_blocks.append(Block(type=BlockType.IMAGE_PLACEHOLDER, visual_key='figure_1_4'))

    return new_blocks


# ---------------------------------------------------------------------------
# Google Docs API Writer
# ---------------------------------------------------------------------------

def retry_api_call(func, max_retries=5):
    for attempt in range(max_retries):
        try:
            return func()
        except HttpError as e:
            if e.resp.status == 429:
                wait = min(2 ** attempt * 10, 60)
                print(f"  Rate limited, waiting {wait}s... (attempt {attempt + 1}/{max_retries})")
                time.sleep(wait)
            else:
                raise
    raise Exception(f"Failed after {max_retries} retries")


class GoogleDocsWriter:
    MAX_BATCH = 50

    def __init__(self, credentials_path):
        creds = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=[
                'https://www.googleapis.com/auth/documents',
                'https://www.googleapis.com/auth/drive',
            ]
        )
        self.docs = build('docs', 'v1', credentials=creds)
        self.drive = build('drive', 'v3', credentials=creds)

    def _batch_update(self, doc_id, requests):
        if not requests:
            return
        for i in range(0, len(requests), self.MAX_BATCH):
            chunk = requests[i:i + self.MAX_BATCH]
            retry_api_call(lambda c=chunk: self.docs.documents().batchUpdate(
                documentId=doc_id, body={'requests': c}
            ).execute())
            if i + self.MAX_BATCH < len(requests):
                time.sleep(2)

    def clear_document(self, doc_id):
        """Clear all existing content from the document."""
        print("  Clearing existing content...")
        doc = retry_api_call(lambda: self.docs.documents().get(documentId=doc_id).execute())
        body = doc['body']['content']
        end_index = body[-1]['endIndex'] - 1 if body else 1
        if end_index > 1:
            self._batch_update(doc_id, [{
                'deleteContentRange': {
                    'range': {'startIndex': 1, 'endIndex': end_index}
                }
            }])

    def insert_text(self, doc_id, text):
        """Insert plain text at the beginning of the document."""
        print(f"  Inserting text ({len(text)} chars)...")
        CHUNK_SIZE = 50000
        insert_pos = 1
        for ci in range(0, len(text), CHUNK_SIZE):
            chunk = text[ci:ci + CHUNK_SIZE]
            retry_api_call(lambda c=chunk, p=insert_pos: self.docs.documents().batchUpdate(
                documentId=doc_id, body={'requests': [{
                    'insertText': {
                        'location': {'index': p},
                        'text': c,
                    }
                }]}
            ).execute())
            insert_pos += len(chunk)
            if ci + CHUNK_SIZE < len(text):
                time.sleep(2)

    def apply_global_style(self, doc_id, text_length):
        """Apply Times New Roman 12pt, 1.5 spacing to the entire document."""
        print("  Applying global style (Times New Roman 12pt, 1.5 spacing)...")
        end = 1 + text_length
        requests = [
            {
                'updateTextStyle': {
                    'range': {'startIndex': 1, 'endIndex': end},
                    'textStyle': {
                        'weightedFontFamily': {'fontFamily': TIMES_NEW_ROMAN},
                        'fontSize': {'magnitude': BODY_SIZE, 'unit': 'PT'},
                    },
                    'fields': 'weightedFontFamily,fontSize',
                }
            },
            {
                'updateParagraphStyle': {
                    'range': {'startIndex': 1, 'endIndex': end},
                    'paragraphStyle': {
                        'lineSpacing': LINE_SPACING,
                        'spaceBelow': {'magnitude': SPACE_AFTER_PT, 'unit': 'PT'},
                        'alignment': 'JUSTIFIED',
                    },
                    'fields': 'lineSpacing,spaceBelow,alignment',
                }
            },
        ]
        self._batch_update(doc_id, requests)

    def apply_text_formatting(self, doc_id, text_formats, base_offset=1):
        """Apply text formatting (bold, italic, font, size, color)."""
        print(f"  Applying {len(text_formats)} text format ranges...")
        requests = []
        for tf in text_formats:
            start = base_offset + tf.start
            end = base_offset + tf.end
            if start >= end:
                continue

            style = {}
            fields = []

            if tf.bold:
                style['bold'] = True
                fields.append('bold')
            if tf.italic:
                style['italic'] = True
                fields.append('italic')
            if tf.font_family:
                style['weightedFontFamily'] = {'fontFamily': tf.font_family}
                fields.append('weightedFontFamily')
            if tf.font_size:
                style['fontSize'] = {'magnitude': tf.font_size, 'unit': 'PT'}
                fields.append('fontSize')
            if tf.fg_color:
                style['foregroundColor'] = {'color': {'rgbColor': tf.fg_color}}
                fields.append('foregroundColor')
            if tf.bg_color:
                style['backgroundColor'] = {'color': {'rgbColor': tf.bg_color}}
                fields.append('backgroundColor')

            if fields:
                requests.append({
                    'updateTextStyle': {
                        'range': {'startIndex': start, 'endIndex': end},
                        'textStyle': style,
                        'fields': ','.join(fields),
                    }
                })

        self._batch_update(doc_id, requests)

    def apply_paragraph_formatting(self, doc_id, para_formats, base_offset=1):
        """Apply paragraph formatting (style, alignment, indent, spacing, bullets)."""
        print(f"  Applying {len(para_formats)} paragraph format ranges...")
        requests = []
        bullet_requests = []

        for pf in para_formats:
            start = base_offset + pf.start
            end = base_offset + pf.end
            if start >= end:
                continue

            # Named style (heading level)
            if pf.named_style:
                requests.append({
                    'updateParagraphStyle': {
                        'range': {'startIndex': start, 'endIndex': end},
                        'paragraphStyle': {'namedStyleType': pf.named_style},
                        'fields': 'namedStyleType',
                    }
                })

            # Other paragraph properties
            para_style = {}
            fields = []

            if pf.alignment:
                para_style['alignment'] = pf.alignment
                fields.append('alignment')
            if pf.first_line_indent_pt is not None:
                para_style['indentFirstLine'] = {'magnitude': pf.first_line_indent_pt, 'unit': 'PT'}
                fields.append('indentFirstLine')
            if pf.indent_start_pt is not None:
                para_style['indentStart'] = {'magnitude': pf.indent_start_pt, 'unit': 'PT'}
                fields.append('indentStart')
            if pf.space_above_pt is not None:
                para_style['spaceAbove'] = {'magnitude': pf.space_above_pt, 'unit': 'PT'}
                fields.append('spaceAbove')
            if pf.space_below_pt is not None:
                para_style['spaceBelow'] = {'magnitude': pf.space_below_pt, 'unit': 'PT'}
                fields.append('spaceBelow')
            if pf.line_spacing is not None:
                para_style['lineSpacing'] = pf.line_spacing
                fields.append('lineSpacing')
            if pf.keep_with_next:
                para_style['keepWithNext'] = True
                fields.append('keepWithNext')

            if fields:
                requests.append({
                    'updateParagraphStyle': {
                        'range': {'startIndex': start, 'endIndex': end},
                        'paragraphStyle': para_style,
                        'fields': ','.join(fields),
                    }
                })

            # Bullets (separate pass)
            if pf.bullet_preset:
                bullet_requests.append({
                    'createParagraphBullets': {
                        'range': {'startIndex': start, 'endIndex': end},
                        'bulletPreset': pf.bullet_preset,
                    }
                })

        self._batch_update(doc_id, requests)
        if bullet_requests:
            time.sleep(1)
            self._batch_update(doc_id, bullet_requests)

    def insert_images(self, doc_id, images, base_offset=1):
        """Insert images from last to first to avoid index shifting."""
        if not images:
            return
        print(f"  Inserting {len(images)} images...")
        # Sort by text_offset descending
        sorted_images = sorted(images, key=lambda img: img.text_offset, reverse=True)
        for img in sorted_images:
            insert_at = base_offset + img.text_offset
            try:
                retry_api_call(lambda idx=insert_at, u=img.url, w=img.width, h=img.height:
                    self.docs.documents().batchUpdate(
                        documentId=doc_id, body={'requests': [{
                            'insertInlineImage': {
                                'location': {'index': idx},
                                'uri': u,
                                'objectSize': {
                                    'width': {'magnitude': w, 'unit': 'PT'},
                                    'height': {'magnitude': h, 'unit': 'PT'},
                                }
                            }
                        }]}
                    ).execute()
                )
                print(f"    Inserted image at offset {img.text_offset}: {img.url}")
                time.sleep(2)
            except Exception as e:
                print(f"    Warning: Failed to insert image at offset {img.text_offset}: {e}")

    def insert_tables(self, doc_id, tables, base_offset=1):
        """Insert tables from last to first."""
        if not tables:
            return
        print(f"  Inserting {len(tables)} tables...")
        sorted_tables = sorted(tables, key=lambda t: t['text_offset'], reverse=True)
        for table_info in sorted_tables:
            self._insert_single_table(doc_id, table_info, base_offset)
            time.sleep(2)

    def _insert_single_table(self, doc_id, table_info, base_offset):
        rows = table_info['rows']
        if not rows:
            return

        insert_at = base_offset + table_info['text_offset']
        n_rows = len(rows)
        n_cols = max(len(r) for r in rows)

        # Delete the placeholder newline
        try:
            self._batch_update(doc_id, [{
                'deleteContentRange': {
                    'range': {'startIndex': insert_at, 'endIndex': insert_at + 1}
                }
            }])
        except Exception:
            pass

        # Insert table
        retry_api_call(lambda: self.docs.documents().batchUpdate(
            documentId=doc_id, body={'requests': [{
                'insertTable': {
                    'rows': n_rows,
                    'columns': n_cols,
                    'location': {'index': insert_at},
                }
            }]}
        ).execute())

        # Read document to get table cell indices
        doc = retry_api_call(lambda: self.docs.documents().get(documentId=doc_id).execute())
        body = doc['body']['content']

        table_element = None
        for element in body:
            if 'table' in element:
                if element['startIndex'] >= insert_at - 2:
                    table_element = element
                    break

        if not table_element:
            print("    Warning: Could not find inserted table")
            return

        table = table_element['table']

        # Fill cells from last to first
        cell_ops = []
        for row_idx in range(n_rows):
            for col_idx in range(n_cols):
                cell_text = rows[row_idx][col_idx] if col_idx < len(rows[row_idx]) else ''
                cell_text = cell_text.strip()
                if not cell_text:
                    continue
                try:
                    cell_content = table['tableRows'][row_idx]['tableCells'][col_idx]['content']
                    cell_start = cell_content[0]['startIndex']
                    cell_ops.append((cell_start, cell_text, row_idx == 0))
                except (IndexError, KeyError):
                    continue

        cell_ops.sort(key=lambda x: x[0], reverse=True)

        requests = []
        for cell_start, cell_text, is_header in cell_ops:
            requests.append({
                'insertText': {
                    'location': {'index': cell_start},
                    'text': cell_text,
                }
            })

        if requests:
            self._batch_update(doc_id, requests)

        # Now apply formatting to header row (bold) and set font
        # Re-read to get updated indices
        doc = retry_api_call(lambda: self.docs.documents().get(documentId=doc_id).execute())
        body = doc['body']['content']
        table_element = None
        for element in body:
            if 'table' in element:
                if element['startIndex'] >= insert_at - 2:
                    table_element = element
                    break

        if table_element:
            table = table_element['table']
            fmt_requests = []
            for row_idx in range(len(table['tableRows'])):
                row = table['tableRows'][row_idx]
                for cell in row['tableCells']:
                    for content in cell['content']:
                        if 'paragraph' in content:
                            p = content['paragraph']
                            p_start = content['startIndex']
                            p_end = content['endIndex']
                            # Set Times New Roman 12pt for all cells
                            fmt_requests.append({
                                'updateTextStyle': {
                                    'range': {'startIndex': p_start, 'endIndex': p_end},
                                    'textStyle': {
                                        'weightedFontFamily': {'fontFamily': TIMES_NEW_ROMAN},
                                        'fontSize': {'magnitude': BODY_SIZE, 'unit': 'PT'},
                                    },
                                    'fields': 'weightedFontFamily,fontSize',
                                }
                            })
                            # Bold for header row
                            if row_idx == 0:
                                fmt_requests.append({
                                    'updateTextStyle': {
                                        'range': {'startIndex': p_start, 'endIndex': p_end},
                                        'textStyle': {'bold': True},
                                        'fields': 'bold',
                                    }
                                })
            if fmt_requests:
                self._batch_update(doc_id, fmt_requests)


# ---------------------------------------------------------------------------
# Main publishing function
# ---------------------------------------------------------------------------

def publish_chapter1(doc_id):
    print("=" * 60)
    print("Publishing Chapter 1: Introduction")
    print(f"Target doc: https://docs.google.com/document/d/{doc_id}/edit")
    print("=" * 60)

    # Step 1: Read and parse markdown
    print("\n[1/7] Reading and parsing chapter markdown...")
    with open(CHAPTER_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = parse_markdown_chapter(content)
    print(f"  Parsed {len(blocks)} blocks")

    # Step 2: Insert visual markers
    print("\n[2/7] Inserting visual placeholders...")
    blocks = insert_visual_markers(blocks)
    print(f"  Total blocks after visual insertion: {len(blocks)}")

    # Step 2.5: Humanize body text paragraphs
    print("\n[2.5/7] Applying text humanization...")
    humanized_count = 0
    skipped_types = {BlockType.HEADING, BlockType.TABLE, BlockType.CODE_BLOCK,
                     BlockType.MATH_BLOCK, BlockType.CAPTION, BlockType.FOOTNOTE,
                     BlockType.HORIZONTAL_RULE, BlockType.IMAGE_PLACEHOLDER}
    for block in blocks:
        if block.type == BlockType.PARAGRAPH:
            # Skip paragraphs that are references (start with [number])
            if re.match(r'^\[\d+\]', block.raw_text.strip()):
                continue
            # Skip bold-only paragraphs (objective/contribution descriptions)
            if block.raw_text.strip().startswith('**') and block.raw_text.strip().count('**') >= 2:
                # These are like sub-headings (e.g., "**Objective 1:...**")
                # Only humanize if there's substantial non-bold text after
                pass
            humanized = humanize_paragraph(block.raw_text)
            if humanized != block.raw_text:
                block.raw_text = humanized
                block.spans = parse_inline(humanized)
                humanized_count += 1
    print(f"  Humanized {humanized_count} paragraphs (out of {sum(1 for b in blocks if b.type == BlockType.PARAGRAPH)} total)")

    # Step 3: Build document structure
    print("\n[3/7] Building document structure...")
    builder = ChapterBuilder()

    for idx, block in enumerate(blocks):
        if block.type == BlockType.HEADING:
            builder.add_heading(block)
        elif block.type == BlockType.PARAGRAPH:
            builder.add_paragraph(block)
        elif block.type == BlockType.CAPTION:
            raw = block.raw_text
            if 'Table 1.1' in raw:
                builder.add_image('table_1_1')
            else:
                builder.add_caption(block)
        elif block.type == BlockType.TABLE:
            # Skip markdown table if we already inserted the Table 1.1 image
            if idx > 0 and blocks[idx - 1].type == BlockType.CAPTION and 'Table 1.1' in blocks[idx - 1].raw_text:
                continue
            builder.add_table_placeholder(block)
        elif block.type == BlockType.CODE_BLOCK:
            builder.add_code_block(block)
        elif block.type == BlockType.MATH_BLOCK:
            builder.add_math_block(block)
        elif block.type == BlockType.UNORDERED_LIST:
            builder.add_list(block, ordered=False)
        elif block.type == BlockType.ORDERED_LIST:
            builder.add_list(block, ordered=True)
        elif block.type == BlockType.HORIZONTAL_RULE:
            builder.add_horizontal_rule()
        elif block.type == BlockType.FOOTNOTE:
            builder.add_footnote(block)
        elif block.type == BlockType.IMAGE_PLACEHOLDER:
            if block.visual_key:
                builder.add_image(block.visual_key)

    full_text = builder.get_full_text()
    print(f"  Total text: {len(full_text)} chars")
    print(f"  Text format ranges: {len(builder.text_formats)}")
    print(f"  Paragraph format ranges: {len(builder.para_formats)}")
    print(f"  Tables: {len(builder.tables)}")
    print(f"  Images: {len(builder.images)}")

    # Step 4: Connect to Google Docs and clear
    print("\n[4/7] Connecting to Google Docs API...")
    writer = GoogleDocsWriter(CREDENTIALS_PATH)
    writer.clear_document(doc_id)

    # Step 5: Insert plain text
    print("\n[5/7] Inserting text content...")
    writer.insert_text(doc_id, full_text)

    # Step 6: Apply formatting
    print("\n[6/7] Applying formatting...")
    text_len = len(full_text)
    writer.apply_global_style(doc_id, text_len)
    time.sleep(1)
    writer.apply_text_formatting(doc_id, builder.text_formats)
    time.sleep(1)
    writer.apply_paragraph_formatting(doc_id, builder.para_formats)

    # Step 7: Insert images and tables
    print("\n[7/7] Inserting images and tables...")
    writer.insert_images(doc_id, builder.images)
    if builder.tables:
        writer.insert_tables(doc_id, builder.tables)

    print("\n" + "=" * 60)
    print("Chapter 1 published successfully!")
    print(f"View at: https://docs.google.com/document/d/{doc_id}/edit")
    print("=" * 60)


if __name__ == '__main__':
    import sys
    doc_id = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DOC_ID
    publish_chapter1(doc_id)