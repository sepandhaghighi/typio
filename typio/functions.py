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
from .params import INVALID_END_ERROR
from .errors import TypioError


def _validate(
    text: Any,
    delay: Any,
    jitter: Any,
    mode: Any,
    end: Any,
    file: Any,
) -> str:
    """
    Validate and normalize inputs for typing operations.

    :param text: text to be printed
    :param delay: base delay (in seconds) between emitted units
    :param jitter: random jitter added/subtracted from delay
    :param mode: typing mode controlling emission granularity
    :param end: end character(s)
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

    if not isinstance(end, str):
        raise TypioError(INVALID_END_ERROR)

    if file is not None and not hasattr(file, "write"):
        raise TypioError(INVALID_FILE_ERROR)
    text = f"{text}{end}"
    return text


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
        self._delay = delay
        self._jitter = jitter
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

    def _sleep(self, delay: Optional[float] = None, jitter: Optional[float] = None) -> None:
        """
        Sleep for a given delay with optional random jitter.

        :param delay: base delay (in seconds) between emitted units
        :param jitter: random jitter added/subtracted from delay
        """
        delay_ = delay or self._delay
        jitter_ = jitter or self._jitter
        if delay_ <= 0:
            return
        if jitter_:
            delay_ += random.uniform(-jitter_, jitter_)
            delay_ = max(0, delay_)
        time.sleep(delay_)

    def _emit(self, part: str) -> None:
        """
        Emit a text fragment.

        :param part: text fragment to write
        """
        self.out.write(part)
        self.out.flush()

    def _mode_char(self, text: str) -> None:
        """
        Emit text character by character.

        :param text: text to emit
        """
        for c in text:
            self._emit(c)
            self._sleep()

    def _mode_word(self, text: str) -> None:
        """
        Emit text word by word, preserving whitespace.

        :param text: text to emit
        """
        for w in re.findall(r"\S+|\s+", text):
            self._emit(w)
            self._sleep()

    def _mode_line(self, text: str) -> None:
        """
        Emit text line by line.

        :param text: text to emit
        """
        for line in text.splitlines(True):
            self._emit(line)
            self._sleep()

    def _mode_sentence(self, text: str) -> None:
        """
        Emit text character by character with longer pauses after sentence-ending punctuation.

        :param text: text to emit
        """
        for c in text:
            self._emit(c)
            self._sleep()
            if c in ".!?":
                self._sleep(self._delay * 4, self._jitter)

    def _mode_typewriter(self, text: str) -> None:
        """
        Emit text character by character with longer pauses after newlines.

        :param text: text to emit
        """
        for c in text:
            self._emit(c)
            self._sleep()
            if c == "\n":
                self._sleep(self._delay * 5, self._jitter)

    def _mode_adaptive(self, text: str) -> None:
        """
        Emit text with adaptive delays based on character type.

        :param text: text to emit
        """
        for c in text:
            d = self._delay * (
                0.3 if c.isspace()
                else 1.5 if not c.isalnum()
                else 1
            )
            self._emit(c)
            self._sleep(delay=d)


def type_print(
        text: str,
        *,
        delay: float = 0.04,
        jitter: float = 0,
        end: str = "\n",
        mode: TypeMode = TypeMode.CHAR,
        file: Optional[TextIOBase] = None) -> None:
    """
    Print text with typing effects.

    :param text: text to be printed
    :param delay: base delay (in seconds) between emitted units
    :param jitter: random jitter added/subtracted from delay
    :param end: end character(s)
    :param mode: typing mode controlling emission granularity
    :param file: output stream supporting a write() method
    """
    text = _validate(text, delay, jitter, mode, end, file)
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
    _validate("", delay, jitter, mode, "", sys.stdout)

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
