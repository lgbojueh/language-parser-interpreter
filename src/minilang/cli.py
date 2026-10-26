from __future__ import annotations

import argparse
import pprint
import sys
from pathlib import Path

from .errors import MiniLangError
from .interpreter import Interpreter
from .lexer import Lexer
from .parser import Parser


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="minilang",
        description="Run a MiniLang source file.",
    )
    parser.add_argument("file", type=Path, help="Path to a .mini source file.")
    parser.add_argument("--tokens", action="store_true", help="Print lexer tokens.")
    parser.add_argument("--ast", action="store_true", help="Pretty-print the AST.")
    parser.add_argument(
        "--no-run",
        action="store_true",
        help="Parse the program without executing it.",
    )
    return parser


def run_source(source: str, *, show_tokens=False, show_ast=False, no_run=False):
    tokens = Lexer(source).scan_tokens()

    if show_tokens:
        for token in tokens:
            print(token)

    program = Parser(tokens).parse()

    if show_ast:
        pprint.pp(program, width=100)

    if not no_run:
        Interpreter().execute(program)

    return program


def main() -> int:
    args = build_parser().parse_args()

    try:
        source = args.file.read_text(encoding="utf-8")
        run_source(
            source,
            show_tokens=args.tokens,
            show_ast=args.ast,
            no_run=args.no_run,
        )
    except FileNotFoundError:
        print(f"error: file not found: {args.file}", file=sys.stderr)
        return 2
    except MiniLangError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
