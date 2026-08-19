# -*- coding: utf-8 -*-
"""typio cli."""

import sys
import argparse
from typing import Any
from .params import TypeMode, TYPIO_OVERVIEW, TYPIO_VERSION
from .params import INVALID_NON_NEGATIVE_NUMBER_ERROR, EXIT_MESSAGE
from .functions import type_print


def _validate_non_negative_number(value: Any) -> float:
    """
    Validate non-negative number.

    :param value: input value
    """
    try:
        number = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(INVALID_NON_NEGATIVE_NUMBER_ERROR.format(value=value))

    if number < 0:
        raise argparse.ArgumentTypeError(INVALID_NON_NEGATIVE_NUMBER_ERROR.format(value=value))
    return number


def _parse_args() -> argparse.Namespace:
    """Parse arguments."""
    parser = argparse.ArgumentParser(
        prog="typio",
        description="Typio: Make Your Terminal Type Like a Human"
    )

    parser.add_argument(
        "text",
        type=str,
        nargs="?",
        help="Text to be printed",
    )

    parser.add_argument(
        "--version",
        action="store_true",
        help="Version",
    )

    parser.add_argument(
        "--text",
        type=str,
        help="Text to be printed",
        dest="text_optional",
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
        help="Ending character(s)",
    )

    parser.add_argument(
        "--mode",
        type=str.lower,
        choices=[m.value for m in TypeMode],
        default=TypeMode.CHAR.value,
        help="Typing mode",
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducibility",
    )

    args = parser.parse_args()
    return args


def _run(args: argparse.Namespace) -> None:
    """
    Run typio CLI.

    :param args: arguments
    """
    if args.version:
        print(TYPIO_VERSION)
        return

    text = args.text
    if args.text_optional is not None:
        text = args.text_optional
    if text is None:
        text = TYPIO_OVERVIEW
    type_print(
        text=text,
        delay=args.delay,
        jitter=args.jitter,
        end=args.end,
        mode=TypeMode(args.mode),
        seed=args.seed,
    )


def main() -> None:
    """CLI main function."""
    try:
        args = _parse_args()
        _run(args)
    except (KeyboardInterrupt, EOFError):
        print(EXIT_MESSAGE)
        sys.exit(1)
