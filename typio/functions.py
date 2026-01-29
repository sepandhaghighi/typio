# -*- coding: utf-8 -*-
"""typio functions."""

import sys
import time
import random
import re
from functools import wraps
from io import TextIOBase
from typing import Any, Callable, Optional
from .params import TypeMode
from .params import INVALID_TEXT_ERROR, INVALID_BYTE_ERROR, INVALID_DELAY_ERROR
from .params import INVALID_JITTER_ERROR, INVALID_MODE_ERROR, INVALID_FILE_ERROR
from .errors import TypioError


def _validate(
    text: Any,
    delay: Any,
    jitter: Any,
    mode: Any,
    file: Any,
) -> str:
    """
    Validate and normalize inputs for typing operations.

    :param text: text to be printed
    :param delay: base delay (in seconds) between emitted units
    :param jitter: random jitter added/subtracted from delay
    :param mode: typing mode controlling emission granularity
    :param file: output stream supporting a write() method
    """
    if not isinstance(text, (str, bytes)):
        raise TypioError(INVALID_TEXT_ERROR)

    if isinstance(text, bytes):
        try:
            text = text.decode()
        except Exception:
            raise TypioError(INVALID_BYTE_ERROR)

    if not isinstance(delay, (int, float)) or delay < 0:
        raise TypioError(INVALID_DELAY_ERROR)

    if not isinstance(jitter, (int, float)) or jitter < 0:
        raise TypioError(INVALID_JITTER_ERROR)

    if not isinstance(mode, TypeMode):
        raise TypioError(INVALID_MODE_ERROR)

    if file is not None and not hasattr(file, "write"):
        raise TypioError(INVALID_FILE_ERROR)

    return text


def _sleep(delay: float, jitter: float) -> None:
    """
    Sleep for a given delay with optional random jitter.

    :param delay: base delay (in seconds) between emitted units
    :param jitter: random jitter added/subtracted from delay
    """
    if delay <= 0:
        return
    if jitter:
        delay += random.uniform(-jitter, jitter)
        delay = max(0, delay)
    time.sleep(delay)


class _TypioPrinter:
    """File-like object that emits text with typing effects."""

    def __init__(self, *, delay: float, jitter: float, mode: TypeMode, out: TextIOBase) -> None:
        """
        Initialize the typing printer.

        :param delay: base delay (in seconds) between emitted units
        :param jitter: random jitter added/subtracted from delay
        :param mode: typing mode controlling emission granularity
        :param out: underlying output stream
        """
        self.delay = delay
        self.jitter = jitter
        self.mode = mode
        self.out = out

    def write(self, text: str) -> None:
        """
        Write text using the configured typing mode.

        :param text: text to be written
        """
        handler = getattr(self, "_mode_{mode}".format(mode=self.mode.value))
        handler(text)

    def flush(self) -> None:
        """Flush the underlying output stream."""
        self.out.flush()

    def _emit(self, part: str, delay: Optional[float] = None) -> None:
        """
        Emit a text fragment and apply delay.

        :param part: text fragment to write
        :param delay: optional override delay for this fragment
        """
        self.out.write(part)
        self.out.flush()
        _sleep(delay if delay is not None else self.delay, self.jitter)

    def _mode_char(self, text: str) -> None:
        """
        Emit text character by character.

        :param text: text to emit
        """
        for c in text:
            self._emit(c)

    def _mode_word(self, text: str) -> None:
        """
        Emit text word by word, preserving whitespace.

        :param text: text to emit
        """
        for w in re.findall(r"\S+|\s+", text):
            self._emit(w)

    def _mode_line(self, text: str) -> None:
        """
        Emit text line by line.

        :param text: text to emit
        """
        for line in text.splitlines(True):
            self._emit(line)

    def _mode_sentence(self, text: str) -> None:
        """
        Emit text character by character with longer pauses after sentence-ending punctuation.

        :param text: text to emit
        """
        for c in text:
            self._emit(c)
            if c in ".!?":
                _sleep(self.delay * 4, self.jitter)

    def _mode_typewriter(self, text: str) -> None:
        """
        Emit text character by character with longer pauses after newlines.

        :param text: text to emit
        """
        for c in text:
            self._emit(c)
            if c == "\n":
                _sleep(self.delay * 5, self.jitter)

    def _mode_adaptive(self, text: str) -> None:
        """
        Emit text with adaptive delays based on character type.

        :param text: text to emit
        """
        for c in text:
            d = self.delay * (
                0.3 if c.isspace()
                else 1.5 if not c.isalnum()
                else 1
            )
            self._emit(c, d)


def type_print(
        text: str,
        *,
        delay: float = 0.04,
        jitter: float = 0,
        mode: TypeMode = TypeMode.CHAR,
        file: Optional[TextIOBase] = None):
    """
    Print text with typing effects.

    :param text: text to be printed
    :param delay: base delay (in seconds) between emitted units
    :param jitter: random jitter added/subtracted from delay
    :param mode: typing mode controlling emission granularity
    :param file: output stream supporting a write() method
    """
    text = _validate(text, delay, jitter, mode, file)
    out = file or sys.stdout

    printer = _TypioPrinter(
        delay=delay,
        jitter=jitter,
        mode=mode,
        out=out,
    )
    printer.write(text)
    printer.flush()


def typestyle(
    *,
    delay: float = 0.04,
    jitter: float = 0,
        mode: TypeMode = TypeMode.CHAR) -> Callable:
    """
    Apply typing effects to all print() calls inside the decorated function.

    :param delay: base delay (in seconds) between emitted units
    :param jitter: random jitter added/subtracted from delay
    :param mode: typing mode controlling emission granularity
    """
    _validate("", delay, jitter, mode, sys.stdout)

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: list, **kwargs: dict) -> Any:
            old_stdout = sys.stdout
            try:
                sys.stdout = _TypioPrinter(
                    delay=delay,
                    jitter=jitter,
                    mode=mode,
                    out=old_stdout,
                )
                return func(*args, **kwargs)
            finally:
                sys.stdout = old_stdout

        return wrapper

    return decorator
