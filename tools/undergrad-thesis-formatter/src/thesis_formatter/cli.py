from __future__ import annotations

import argparse
import json
from pathlib import Path

from .analyzer import analyze_template
from .formatter import apply_template_format


def _analyze(args: argparse.Namespace) -> None:
    profile = analyze_template(args.template)
    print(json.dumps(profile.to_dict(), ensure_ascii=False, indent=2))


def _apply(args: argparse.Namespace) -> None:
    result = apply_template_format(
        template_path=args.template,
        thesis_path=args.input,
        output_path=args.output,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="thesis-format",
        description="Analyze a school DOCX template and apply its thesis formatting.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze_parser = subparsers.add_parser("analyze", help="Analyze a school template DOCX.")
    analyze_parser.add_argument("template", type=Path)
    analyze_parser.set_defaults(func=_analyze)

    apply_parser = subparsers.add_parser("apply", help="Apply template formatting to a thesis DOCX.")
    apply_parser.add_argument("--template", required=True, type=Path)
    apply_parser.add_argument("--input", required=True, type=Path)
    apply_parser.add_argument("--output", required=True, type=Path)
    apply_parser.set_defaults(func=_apply)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
