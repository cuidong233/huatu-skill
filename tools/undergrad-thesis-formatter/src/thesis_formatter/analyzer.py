from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from docx import Document
from docx.enum.style import WD_STYLE_TYPE


BODY_CANDIDATES = ("Normal", "正文", "Body Text")
HEADING_CANDIDATES = {
    1: ("Heading 1", "标题 1", "标题1", "一级标题"),
    2: ("Heading 2", "标题 2", "标题2", "二级标题"),
    3: ("Heading 3", "标题 3", "标题3", "三级标题"),
}


@dataclass
class StyleSnapshot:
    name: str
    font_name: str | None
    font_size_pt: float | None
    bold: bool | None
    italic: bool | None
    alignment: str | None
    first_line_indent_pt: float | None
    line_spacing: float | None
    space_before_pt: float | None
    space_after_pt: float | None


@dataclass
class PageSnapshot:
    width_cm: float | None
    height_cm: float | None
    top_margin_cm: float | None
    bottom_margin_cm: float | None
    left_margin_cm: float | None
    right_margin_cm: float | None
    header_distance_cm: float | None
    footer_distance_cm: float | None


@dataclass
class TemplateProfile:
    path: str
    page: PageSnapshot
    body_style: StyleSnapshot | None
    heading_styles: dict[int, StyleSnapshot]
    paragraph_style_count: int
    sample_headings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _length_to_cm(value) -> float | None:
    if value is None:
        return None
    return round(value.cm, 2)


def _length_to_pt(value) -> float | None:
    if value is None:
        return None
    return round(value.pt, 2)


def _style_snapshot(style) -> StyleSnapshot:
    paragraph_format = style.paragraph_format
    font = style.font
    return StyleSnapshot(
        name=style.name,
        font_name=font.name,
        font_size_pt=_length_to_pt(font.size),
        bold=font.bold,
        italic=font.italic,
        alignment=str(paragraph_format.alignment) if paragraph_format.alignment else None,
        first_line_indent_pt=_length_to_pt(paragraph_format.first_line_indent),
        line_spacing=paragraph_format.line_spacing,
        space_before_pt=_length_to_pt(paragraph_format.space_before),
        space_after_pt=_length_to_pt(paragraph_format.space_after),
    )


def _find_style(document: Document, names: tuple[str, ...]):
    for name in names:
        try:
            return document.styles[name]
        except KeyError:
            continue
    return None


def analyze_template(template_path: str | Path) -> TemplateProfile:
    path = Path(template_path)
    document = Document(path)
    section = document.sections[0]

    body_style = _find_style(document, BODY_CANDIDATES)
    heading_styles = {}
    for level, names in HEADING_CANDIDATES.items():
        style = _find_style(document, names)
        if style is not None:
            heading_styles[level] = _style_snapshot(style)

    paragraph_styles = [
        style
        for style in document.styles
        if style.type == WD_STYLE_TYPE.PARAGRAPH
    ]

    sample_headings = []
    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if text and paragraph.style and "heading" in paragraph.style.name.lower():
            sample_headings.append(text)
        if len(sample_headings) >= 12:
            break

    return TemplateProfile(
        path=str(path),
        page=PageSnapshot(
            width_cm=_length_to_cm(section.page_width),
            height_cm=_length_to_cm(section.page_height),
            top_margin_cm=_length_to_cm(section.top_margin),
            bottom_margin_cm=_length_to_cm(section.bottom_margin),
            left_margin_cm=_length_to_cm(section.left_margin),
            right_margin_cm=_length_to_cm(section.right_margin),
            header_distance_cm=_length_to_cm(section.header_distance),
            footer_distance_cm=_length_to_cm(section.footer_distance),
        ),
        body_style=_style_snapshot(body_style) if body_style is not None else None,
        heading_styles=heading_styles,
        paragraph_style_count=len(paragraph_styles),
        sample_headings=sample_headings,
    )
