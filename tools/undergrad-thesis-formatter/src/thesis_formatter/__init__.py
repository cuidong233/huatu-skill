"""Tools for applying undergraduate thesis DOCX formatting."""

__all__ = ["analyze_template", "apply_template_format"]

from .analyzer import analyze_template
from .formatter import apply_template_format
