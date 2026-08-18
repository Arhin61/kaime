"""Build the KTU project report as a formatted Word document.

Run with:  uv run --with python-docx python report/build_docx.py

Formatting follows the Computer Science Department guidelines:
Times New Roman 12 pt, 1.5 line spacing, justified body text, centred bold major
headings, left-aligned bold numbered sub-headings (max three levels), each chapter on
a new page, roman numerals for preliminary pages and arabic numerals from Chapter One.
"""

from __future__ import annotations

import struct
import sys
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from content_back import APPENDICES, REFERENCES  # noqa: E402
from content_ch3 import CHAPTER_THREE  # noqa: E402
from content_ch4 import CHAPTER_FOUR  # noqa: E402
from content_ch5 import CHAPTER_FIVE  # noqa: E402
from content_ch12 import CHAPTER_ONE, CHAPTER_TWO  # noqa: E402
from content_front import ABSTRACT, ACKNOWLEDGEMENTS, DECLARATION, TITLE_PAGE  # noqa: E402

FONT = "Times New Roman"
MONO = "Courier New"
BODY_PT = 12
PNG_DIR = HERE / "diagrams" / "png"
OUT = HERE / "Kaime_Project_Report.docx"

# Usable text width with 1 inch left/right margins on A4.
MAX_IMG_W = 6.0
MAX_IMG_H = 7.6


# --------------------------------------------------------------------------- #
# low-level helpers
# --------------------------------------------------------------------------- #
def png_size(path: Path) -> tuple[int, int]:
    """Width and height of a PNG, read from the IHDR chunk."""
    with path.open("rb") as fh:
        head = fh.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"not a PNG: {path}")
    return struct.unpack(">II", head[16:24])


def add_field(paragraph, instruction: str, placeholder: str = "Update this field (F9)"):
    """Insert a Word field code such as PAGE or TOC."""
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = instruction
    sep = OxmlElement("w:fldChar")
    sep.set(qn("w:fldCharType"), "separate")
    text = OxmlElement("w:t")
    text.text = placeholder
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    for node in (begin, instr, sep, text, end):
        run._r.append(node)
    return run


def set_page_numbering(section, fmt: str, start: int | None = None):
    pg = OxmlElement("w:pgNumType")
    pg.set(qn("w:fmt"), fmt)
    if start is not None:
        pg.set(qn("w:start"), str(start))
    section._sectPr.append(pg)


def add_footer_page_number(section):
    section.footer.is_linked_to_previous = False
    para = section.footer.paragraphs[0]
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.paragraph_format.space_before = Pt(0)
    para.paragraph_format.space_after = Pt(0)
    para.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    add_field(para, " PAGE ", "1")
    for run in para.runs:
        run.font.name = FONT
        run.font.size = Pt(BODY_PT)


def clear_footer(section):
    section.footer.is_linked_to_previous = False
    for para in section.footer.paragraphs:
        for run in list(para.runs):
            run._r.getparent().remove(run._r)


def shade(cell_or_para, hex_fill: str):
    el = OxmlElement("w:shd")
    el.set(qn("w:val"), "clear")
    el.set(qn("w:color"), "auto")
    el.set(qn("w:fill"), hex_fill)
    target = cell_or_para._tc.get_or_add_tcPr() if hasattr(cell_or_para, "_tc") \
        else cell_or_para._p.get_or_add_pPr()
    target.append(el)


def repeat_header_row(row):
    tr_pr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:tblHeader")
    el.set(qn("w:val"), "true")
    tr_pr.append(el)


# --------------------------------------------------------------------------- #
# document set-up
# --------------------------------------------------------------------------- #
def build_styles(doc: Document):
    normal = doc.styles["Normal"]
    normal.font.name = FONT
    normal.font.size = Pt(BODY_PT)
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    pf = normal.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    pf.space_after = Pt(10)
    pf.space_before = Pt(0)
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # Heading 1 -> chapter and major headings: centred, bold.
    h1 = doc.styles["Heading 1"]
    h1.font.name = FONT
    h1.font.size = Pt(BODY_PT)
    h1.font.bold = True
    h1.font.color.rgb = RGBColor(0, 0, 0)
    h1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    h1.paragraph_format.space_before = Pt(0)
    h1.paragraph_format.space_after = Pt(14)
    h1.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    h1.paragraph_format.keep_with_next = True

    for name, before, after in (("Heading 2", 14, 8), ("Heading 3", 12, 6)):
        style = doc.styles[name]
        style.font.name = FONT
        style.font.size = Pt(BODY_PT)
        style.font.bold = True
        style.font.italic = False
        style.font.color.rgb = RGBColor(0, 0, 0)
        style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.space_after = Pt(after)
        style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
        style.paragraph_format.keep_with_next = True

    def caption_style(name: str):
        style = doc.styles.add_style(name, 1)  # WD_STYLE_TYPE.PARAGRAPH
        style.base_style = doc.styles["Normal"]
        style.font.name = FONT
        style.font.size = Pt(11)
        style.font.bold = False
        style.font.italic = False
        style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
        style.paragraph_format.space_before = Pt(4)
        style.paragraph_format.space_after = Pt(12)
        style.paragraph_format.keep_with_next = False
        return style

    caption_style("FigureCaption")
    tc = caption_style("TableCaption")
    tc.paragraph_format.space_after = Pt(4)
    tc.paragraph_format.keep_with_next = True

    code = doc.styles.add_style("CodeBlock", 1)
    code.base_style = doc.styles["Normal"]
    code.font.name = MONO
    code.element.rPr.rFonts.set(qn("w:ascii"), MONO)
    code.element.rPr.rFonts.set(qn("w:hAnsi"), MONO)
    code.font.size = Pt(8)
    code.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    code.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    code.paragraph_format.space_before = Pt(0)
    code.paragraph_format.space_after = Pt(0)
    code.paragraph_format.left_indent = Cm(0.3)

    note = doc.styles.add_style("AuthorNote", 1)
    note.base_style = doc.styles["Normal"]
    note.font.name = FONT
    note.font.size = Pt(10)
    note.font.italic = True
    note.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    note.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    note.paragraph_format.left_indent = Cm(0.6)
    note.paragraph_format.right_indent = Cm(0.6)
    note.paragraph_format.space_before = Pt(8)
    note.paragraph_format.space_after = Pt(12)

    ref = doc.styles.add_style("ReferenceEntry", 1)
    ref.base_style = doc.styles["Normal"]
    ref.font.name = FONT
    ref.font.size = Pt(BODY_PT)
    ref.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    ref.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    ref.paragraph_format.left_indent = Cm(1.27)
    ref.paragraph_format.first_line_indent = Cm(-1.27)
    ref.paragraph_format.space_after = Pt(10)


def setup_margins(section):
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1.25)
    section.right_margin = Inches(1)


# --------------------------------------------------------------------------- #
# block renderers
# --------------------------------------------------------------------------- #
class Builder:
    def __init__(self, doc: Document):
        self.doc = doc
        self.numbering_restart = True

    # -- text ---------------------------------------------------------------
    def para(self, text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=False, italic=False,
             size=BODY_PT, space_after=None, style=None):
        p = self.doc.add_paragraph(style=style)
        p.alignment = align
        if space_after is not None:
            p.paragraph_format.space_after = Pt(space_after)
        run = p.add_run(text)
        run.font.name = FONT
        run.font.size = Pt(size)
        run.bold = bold
        run.italic = italic
        return p

    def heading(self, text, level):
        h = self.doc.add_heading(text, level=level)
        for run in h.runs:
            run.font.name = FONT
            run.font.size = Pt(BODY_PT)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0, 0, 0)
        return h

    def page_break(self):
        self.doc.add_page_break()

    # -- lists ---------------------------------------------------------------
    def numbered(self, text):
        p = self.doc.add_paragraph(text, style="List Number")
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
        p.paragraph_format.space_after = Pt(8)
        for run in p.runs:
            run.font.name = FONT
            run.font.size = Pt(BODY_PT)
        return p

    def bulleted(self, text):
        p = self.doc.add_paragraph(text, style="List Bullet")
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
        p.paragraph_format.space_after = Pt(8)
        for run in p.runs:
            run.font.name = FONT
            run.font.size = Pt(BODY_PT)
        return p

    # -- captions ------------------------------------------------------------
    def table_caption(self, number, text):
        p = self.doc.add_paragraph(style="TableCaption")
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(f"Table {number}: ")
        run.bold = True
        run.font.name = FONT
        run.font.size = Pt(11)
        run2 = p.add_run(text)
        run2.font.name = FONT
        run2.font.size = Pt(11)

    def figure_caption(self, number, text):
        p = self.doc.add_paragraph(style="FigureCaption")
        run = p.add_run(f"Figure {number}: ")
        run.bold = True
        run.font.name = FONT
        run.font.size = Pt(11)
        run2 = p.add_run(text)
        run2.font.name = FONT
        run2.font.size = Pt(11)

    # -- tables --------------------------------------------------------------
    def table(self, headers, rows, widths=None, font_size=10):
        t = self.doc.add_table(rows=1, cols=len(headers))
        t.style = "Table Grid"
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        if widths:
            t.autofit = False
            layout = OxmlElement("w:tblLayout")
            layout.set(qn("w:type"), "fixed")
            t._tbl.tblPr.append(layout)
        else:
            t.autofit = True

        hdr = t.rows[0]
        repeat_header_row(hdr)
        for idx, label in enumerate(headers):
            cell = hdr.cells[idx]
            cell.text = ""
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.space_before = Pt(2)
            run = p.add_run(label)
            run.bold = True
            run.font.name = FONT
            run.font.size = Pt(font_size)
            shade(cell, "D9D9D9")

        for row_values in rows:
            cells = t.add_row().cells
            for idx, value in enumerate(row_values):
                cell = cells[idx]
                cell.text = ""
                lines = str(value).split("\n")
                for line_idx, line in enumerate(lines):
                    p = cell.paragraphs[0] if line_idx == 0 else cell.add_paragraph()
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
                    p.paragraph_format.space_after = Pt(2)
                    p.paragraph_format.space_before = Pt(2)
                    run = p.add_run(line)
                    run.font.name = FONT
                    run.font.size = Pt(font_size)

        if widths:
            for idx, width in enumerate(widths):
                t.columns[idx].width = Inches(width)
            for row in t.rows:
                for idx, width in enumerate(widths):
                    row.cells[idx].width = Inches(width)

        self.doc.add_paragraph().paragraph_format.space_after = Pt(6)
        return t

    # -- figures -------------------------------------------------------------
    def figure(self, number, caption, filename):
        path = PNG_DIR / filename
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(2)
        if path.exists():
            w_px, h_px = png_size(path)
            width = MAX_IMG_W
            height = width * h_px / w_px
            if height > MAX_IMG_H:
                height = MAX_IMG_H
                width = height * w_px / h_px
            p.add_run().add_picture(str(path), width=Inches(width))
        else:
            run = p.add_run(f"[MISSING IMAGE: {filename}]")
            run.italic = True
            run.font.name = FONT
        self.figure_caption(number, caption)

    def figure_placeholder(self, number, caption):
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run("[ INSERT SCREENSHOT HERE ]")
        run.italic = True
        run.font.name = FONT
        run.font.size = Pt(11)
        run.font.color.rgb = RGBColor(0x80, 0x80, 0x80)
        self.figure_caption(number, caption)

    # -- code ----------------------------------------------------------------
    def code(self, label, caption, text):
        if label or caption:
            p = self.doc.add_paragraph(style="TableCaption")
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            head = f"{label}: " if label else ""
            run = p.add_run(head)
            run.bold = True
            run.font.name = FONT
            run.font.size = Pt(11)
            run2 = p.add_run(caption)
            run2.font.name = FONT
            run2.font.size = Pt(11)

        lines = text.split("\n")
        for idx, line in enumerate(lines):
            p = self.doc.add_paragraph(style="CodeBlock")
            if idx == 0:
                p.paragraph_format.space_before = Pt(6)
            if idx == len(lines) - 1:
                p.paragraph_format.space_after = Pt(12)
            run = p.add_run(line if line else " ")
            run.font.name = MONO
            run.font.size = Pt(8)
            shade(p, "F2F2F2")

    # -- author note ---------------------------------------------------------
    def note(self, text):
        p = self.doc.add_paragraph(style="AuthorNote")
        run = p.add_run(text)
        run.font.name = FONT
        run.font.size = Pt(10)
        run.italic = True
        run.font.color.rgb = RGBColor(0x99, 0x00, 0x00)
        shade(p, "FFF2CC")

    # -- signature block -----------------------------------------------------
    def signature(self, name, role):
        for label, value in (("Signature", "." * 40), ("Date", "." * 40)):
            p = self.doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(4)
            run = p.add_run(f"{label}: {value}")
            run.font.name = FONT
            run.font.size = Pt(BODY_PT)
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(f"{name}")
        run.bold = True
        run.font.name = FONT
        run.font.size = Pt(BODY_PT)
        p2 = self.doc.add_paragraph()
        p2.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run2 = p2.add_run(f"({role})")
        run2.font.name = FONT
        run2.font.size = Pt(BODY_PT)


# --------------------------------------------------------------------------- #
# generated tables
# --------------------------------------------------------------------------- #
TRACEABILITY = [
    ("FR-01", "Academic terms", "TC-01 to TC-04"),
    ("FR-02", "Student records", "TC-05, TC-06, TC-07, TC-09"),
    ("FR-03", "Student records", "TC-08"),
    ("FR-04", "Course catalogue", "TC-12, TC-13, TC-14"),
    ("FR-05", "Enrolment", "TC-16 to TC-20"),
    ("FR-06", "Timetable", "TC-21, TC-22"),
    ("FR-07", "Timetable", "TC-23 to TC-26"),
    ("FR-08", "Attendance", "TC-27, TC-29, TC-30, TC-31"),
    ("FR-09", "Attendance", "TC-28"),
    ("FR-10", "Attendance", "TC-32, TC-33, TC-34"),
    ("FR-11", "Grading", "TC-35"),
    ("FR-12", "Grading", "TC-36, TC-37"),
    ("FR-13", "Grading", "TC-38, TC-39, TC-40, TC-41"),
    ("FR-14", "Grading", "TC-42 to TC-46, TC-48"),
    ("FR-15", "Grading", "TC-47"),
    ("FR-16", "Fees and billing", "TC-49"),
    ("FR-17", "Fees and billing", "TC-50 to TC-53"),
    ("FR-18", "Fees and billing", "TC-54, TC-55, TC-56"),
    ("FR-19", "Fees and billing", "TC-57, TC-58, TC-59"),
    ("FR-20", "Fees and billing", "TC-60"),
    ("FR-21", "All modules", "TC-04, TC-10, TC-11, TC-15"),
    ("FR-22", "Events", "TC-61, TC-62, TC-69"),
    ("FR-23", "Notifications", "TC-63, TC-64, TC-66 to TC-70, TC-73, TC-74"),
    ("FR-24", "Notifications", "TC-65, TC-78"),
    ("FR-25", "Notifications", "TC-71"),
    ("FR-26", "Notifications", "TC-72"),
    ("FR-27", "Dashboard", "TC-81, TC-82"),
]


# --------------------------------------------------------------------------- #
# rendering
# --------------------------------------------------------------------------- #
def render(builder: Builder, blocks):
    doc = builder.doc
    for block in blocks:
        kind = block[0]

        if kind == "chapter":
            builder.page_break()
            builder.heading(block[1], 1)
            p = doc.paragraphs[-1]
            p.paragraph_format.space_after = Pt(6)
            builder.heading(block[2], 1)

        elif kind == "chapter_single":
            builder.page_break()
            builder.heading(block[1], 1)

        elif kind == "h1":
            builder.heading(block[1], 1)

        elif kind == "h2":
            builder.heading(f"{block[1]} {block[2]}", 2)

        elif kind == "h3":
            builder.heading(f"{block[1]} {block[2]}", 3)

        elif kind == "p":
            builder.para(block[1])

        elif kind == "p_left":
            builder.para(block[1], align=WD_ALIGN_PARAGRAPH.JUSTIFY)

        elif kind == "p_left_italic":
            builder.para(block[1], align=WD_ALIGN_PARAGRAPH.JUSTIFY, italic=True)

        elif kind == "num":
            builder.numbered(block[1])

        elif kind == "bullet":
            builder.bulleted(block[1])

        elif kind == "table":
            builder.table_caption(block[1], block[2])
            widths = block[5] if len(block) > 5 else None
            builder.table(block[3], block[4], widths=widths)

        elif kind == "test_table":
            builder.table_caption(block[1], block[2])
            rows = [[r[0], r[1], r[2], r[3], "[FILL IN]"] for r in block[3]]
            builder.table(
                ["ID", "Req.", "Test description", "Expected outcome", "Result"],
                rows,
                widths=[0.55, 0.55, 1.85, 2.25, 0.8],
                font_size=9,
            )

        elif kind == "results_table":
            builder.table_caption(block[1], block[2])
            builder.table(
                ["Module", "Test cases", "Total", "Passed", "Failed", "Pass rate"],
                block[3],
                widths=[1.5, 1.3, 0.6, 0.7, 0.7, 0.9],
                font_size=10,
            )

        elif kind == "perf_table":
            builder.table_caption(block[1], block[2])
            rows = [[r[0], r[1], r[2]] for r in block[3]]
            builder.table(
                ["Operation", "Requirement", "Mean response time (ms)"],
                rows,
                widths=[3.3, 1.1, 1.6],
                font_size=10,
            )

        elif kind == "traceability_table":
            builder.table_caption(block[1], block[2])
            rows = [[fr, mod, tcs, "[FILL IN]"] for fr, mod, tcs in TRACEABILITY]
            builder.table(
                ["Requirement", "Implementing module", "Verifying test cases", "Status"],
                rows,
                widths=[1.0, 1.5, 2.4, 1.1],
                font_size=9,
            )

        elif kind == "nfr_table":
            builder.table_caption(block[1], block[2])
            builder.table(
                ["ID", "Requirement", "Means of verification", "Assessment"],
                block[3],
                widths=[0.6, 1.7, 2.6, 1.1],
                font_size=9,
            )

        elif kind == "comparison_table":
            builder.table_caption(block[1], block[2])
            builder.table(
                block[3], block[4],
                widths=[1.5, 1.0, 1.15, 0.95, 0.9, 0.9],
                font_size=8,
            )

        elif kind == "appendix_code_list":
            builder.table(["Module", "Content"], block[3],
                          widths=[2.2, 3.8], font_size=10)

        elif kind == "api_table":
            builder.table(["Module", "Endpoints"], block[3],
                          widths=[1.1, 4.9], font_size=9)

        elif kind == "config_table":
            builder.table(["Parameter", "Default", "Purpose"], block[3],
                          widths=[2.2, 1.1, 2.7], font_size=9)

        elif kind == "gantt_table":
            builder.table(
                ["Activity", "Start", "End", "Deliverable"], block[3],
                widths=[2.2, 0.9, 0.9, 2.0], font_size=9,
            )

        elif kind == "code":
            builder.code(block[1], block[2], block[3])

        elif kind == "figure":
            builder.figure(block[1], block[2], block[3])

        elif kind == "figure_placeholder":
            builder.figure_placeholder(block[1], block[2])

        elif kind == "note":
            builder.note(block[1])

        elif kind == "ref":
            p = doc.add_paragraph(style="ReferenceEntry")
            run = p.add_run(block[1])
            run.font.name = FONT
            run.font.size = Pt(BODY_PT)

        elif kind == "sig":
            builder.signature(block[1], block[2])

        elif kind == "spacer":
            for _ in range(block[1]):
                p = doc.add_paragraph()
                p.paragraph_format.space_after = Pt(0)

        elif kind.startswith("title_"):
            render_title_block(builder, block)

        else:
            raise ValueError(f"unknown block type: {kind}")


def render_title_block(builder: Builder, block):
    kind = block[0]
    doc = builder.doc
    if kind == "title_mid_bold_tail":
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(4)
        r1 = p.add_run(block[1][0])
        r1.font.name = FONT
        r1.font.size = Pt(14)
        r2 = p.add_run(block[1][1])
        r2.bold = True
        r2.font.name = FONT
        r2.font.size = Pt(14)
        return

    sizes = {
        "title_big": (24, True),
        "title_mid": (14, False),
        "title_topic": (14, True),
        "title_bold": (13, True),
    }
    size, bold = sizes[kind]
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    run = p.add_run(block[1])
    run.bold = bold
    run.font.name = FONT
    run.font.size = Pt(size)


# --------------------------------------------------------------------------- #
# preliminary sections needing field codes
# --------------------------------------------------------------------------- #
def add_toc(builder: Builder):
    builder.page_break()
    builder.para("TABLE OF CONTENTS", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True,
                 space_after=14)
    p = builder.doc.add_paragraph()
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    add_field(
        p,
        ' TOC \\o "1-3" \\h \\z \\u ',
        "Right-click here and choose Update Field to build the table of contents.",
    )
    for run in p.runs:
        run.font.name = FONT
        run.font.size = Pt(BODY_PT)


def add_list_of(builder: Builder, title: str, style_name: str, note: str):
    builder.page_break()
    builder.para(title, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, space_after=14)
    p = builder.doc.add_paragraph()
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    add_field(p, f' TOC \\h \\z \\t "{style_name},1" ', note)
    for run in p.runs:
        run.font.name = FONT
        run.font.size = Pt(BODY_PT)


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main():
    doc = Document()
    build_styles(doc)
    builder = Builder(doc)

    # --- Section 1: title page, no page number ---------------------------- #
    section1 = doc.sections[0]
    setup_margins(section1)
    clear_footer(section1)
    render(builder, TITLE_PAGE)

    # --- Section 2: preliminaries, lower-roman numerals -------------------- #
    section2 = doc.add_section(WD_SECTION.NEW_PAGE)
    setup_margins(section2)
    set_page_numbering(section2, "lowerRoman", start=2)
    add_footer_page_number(section2)

    render(builder, DECLARATION)
    builder.page_break()
    render(builder, ACKNOWLEDGEMENTS)
    builder.page_break()
    render(builder, ABSTRACT)

    add_toc(builder)
    add_list_of(
        builder,
        "LIST OF FIGURES",
        "FigureCaption",
        "Right-click here and choose Update Field to build the list of figures.",
    )
    add_list_of(
        builder,
        "LIST OF TABLES",
        "TableCaption",
        "Right-click here and choose Update Field to build the list of tables.",
    )

    # --- Section 3: chapters onward, arabic numerals from 1 ---------------- #
    section3 = doc.add_section(WD_SECTION.NEW_PAGE)
    setup_margins(section3)
    set_page_numbering(section3, "decimal", start=1)
    add_footer_page_number(section3)

    # The first chapter block emits its own page break; the new section already
    # begins on a fresh page, so drop that leading break.
    first = CHAPTER_ONE[0]
    builder.heading(first[1], 1)
    doc.paragraphs[-1].paragraph_format.space_after = Pt(6)
    builder.heading(first[2], 1)
    render(builder, CHAPTER_ONE[1:])

    for chapter in (CHAPTER_TWO, CHAPTER_THREE, CHAPTER_FOUR, CHAPTER_FIVE,
                    REFERENCES, APPENDICES):
        render(builder, chapter)

    doc.save(OUT)
    print(f"written: {OUT}")
    print(f"paragraphs: {len(doc.paragraphs)}  tables: {len(doc.tables)}")


if __name__ == "__main__":
    main()
