# -*- coding: utf-8 -*-
"""typio cli."""

import argparse
import sys
from typing import Optional, Any
from .params import TypeMode
from .functions import type_print


def _validate_non_negative_number(value: Any) -> float:
    """
    Validate non-negative number.

    :param value: input value
    """
    try:
        number = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"invalid non-negative number: '{value}'")

    if number < 0:
        raise argparse.ArgumentTypeError(f"invalid non-negative number: '{value}'")
    return number


def _build_parser() -> argparse.ArgumentParser:
    """Build argument parser."""
    parser = argparse.ArgumentParser(
        prog="typio",
        description="Typio: Make Your Terminal Type Like a Human"
    )

    parser.add_argument(
        "--version",
        action="store_true",
        help="Version",
    )

    parser.add_argument(
        "--text",
        type=str,
        default=DEFAULT_TEXT,
        help="Text to be printed",
    )

    parser.add_argument(
        "--delay",
        type=_validate_non_negative_number,
        default=0.04,
        help="Base delay (seconds) between emitted units",
    )

    parser.add_argument(
        "--jitter",
        type=_validate_non_negative_number,
        default=0.0,
        help="Random delay variation (seconds)",
    )

    parser.add_argument(
        "--end",
        type=str,
        default="\n",
        help="End character(s)",
    )

    parser.add_argument(
        "--mode",
        type=str,
        choices=[m.value for m in TypeMode],
        default=TypeMode.CHAR.value,
        help="Typing mode",
    )

    return parser


def main() -> None:
    """CLI main function."""
    parser = _build_parser()
    args = parser.parse_args()

    if args.version:
        print(TYPIO_VERSION)
        return

    type_print(
        text=args.text,
        delay=args.delay,
        jitter=args.jitter,
        end=args.end,
        mode=TypeMode(args.mode),
    )
