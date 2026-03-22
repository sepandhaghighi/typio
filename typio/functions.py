# -*- coding: utf-8 -*-
"""typio functions."""

import sys
import time
import random
import re
from functools import wraps
from io import TextIOBase
from typing import Any, Callable, Optional, Union
from .params import TypeMode, KEY_NEIGHBORS
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
    :param end: ending character(s)
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

    if not isinstance(mode, TypeMode) and not callable(mode):
        raise TypioError(INVALID_MODE_ERROR)

    if not isinstance(end, str):
        raise TypioError(INVALID_END_ERROR)

    if file is not None and not hasattr(file, "write"):
        raise TypioError(INVALID_FILE_ERROR)
    text = f"{text}{end}"
    return text


class _TypioPrinter:
    """File-like object that emits text with typing effects."""

    def __init__(self, *, delay: float, jitter: float, mode: Union[TypeMode, Callable], out: TextIOBase) -> None:
        """
        Initialize the typing printer.

        :param delay: base delay (in seconds) between emitted units
        :param jitter: random jitter added/subtracted from delay
        :param mode: typing mode controlling emission granularity
        :param out: underlying output stream
        """
        self._delay = delay
        self._jitter = jitter
        self._mode = mode
        self._out = out

    def write(self, text: str) -> None:
        """
        Write text using the configured typing mode.

        :param text: text to be written
        """
        if callable(self._mode):
            ctx = TypioContext(self)
            self._mode(ctx, text)
        else:
            handler = getattr(self, "_mode_{mode}".format(mode=self._mode.value.replace('-', '_')))
            handler(text)

    def flush(self) -> None:
        """Flush the underlying output stream."""
        self._out.flush()

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

    def _emit(self, text: str) -> None:
        """
        Emit a text fragment.

        :param text: text fragment to write
        """
        self._out.write(text)
        self._out.flush()

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
                self._sleep(self._delay * 4)

    def _mode_typewriter(self, text: str) -> None:
        """
        Emit text character by character with longer pauses after newlines.

        :param text: text to emit
        """
        for c in text:
            self._emit(c)
            self._sleep()
            if c == "\n":
                self._sleep(self._delay * 5)

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

    def _mode_accelerate(self, text: str) -> None:
        """
        Emit text character by character with progressively decreasing delay.

        :param text: text to emit
        """
        total = len(text)
        for i, c in enumerate(text):
            self._emit(c)
            factor = max(0.2, 1 - (i / total))
            self._sleep(delay=self._delay * factor)

    def _mode_decelerate(self, text: str) -> None:
        """
        Emit text character by character with progressively increasing delay.

        :param text: text to emit
        """
        total = len(text)
        for i, c in enumerate(text):
            self._emit(c)
            factor = max(0.2, i / total)
            self._sleep(delay=self._delay * factor)

    def _mode_burst(self, text: str) -> None:
        """
        Emit text in bursts of characters followed by short pauses.

        :param text: text to emit
        """
        buffer = []
        burst_size = random.randint(3, 8)
        for c in text:
            buffer.append(c)
            if len(buffer) >= burst_size:
                self._emit("".join(buffer))
                buffer.clear()
                self._sleep()
                burst_size = random.randint(3, 8)
        if buffer:
            self._emit("".join(buffer))
            self._sleep()

    def _mode_fat_finger(self, text: str) -> None:
        """
        Emit text mimicking human typos and corrections.

        :param text: text to emit
        """
        i = 0
        while i < len(text):
            char = text[i]
            if char in KEY_NEIGHBORS and random.random() < 0.03:
                wrong_char = random.choice(KEY_NEIGHBORS[char])
                self._emit(wrong_char)
                self._sleep(delay=self._delay * 1.25)
                
                # Type another wrong character with decaying probability
                extra_chars = []
                decay_rate = 0.6
                current_j = i + 1
                while current_j < len(text) and random.random() < (decay_rate ** (len(extra_chars) + 1)):
                    next_char = text[current_j]
                    self._emit(next_char)
                    extra_chars.append(next_char)
                    self._sleep(delay=self._delay * 1.5)
                    current_j += 1

                self._sleep(delay=self._delay * 4)
                total_to_delete = len(extra_chars) + 1
                for _ in range(total_to_delete):
                    self._emit("\b \b")
                    self._sleep(delay=self._delay * 0.75)

                self._sleep(delay=self._delay * 3)
                continue

            self._emit(char)
            self._sleep()
            i += 1

    def _mode_thoughtful(self, text: str) -> None:
        """
        Emit text while pause slightly before long words to simulate thinking.

        :param text: text to emit
        """
        for token in re.findall(r"\S+|\s+", text):
            if token.strip() and len(token.strip()) > 6:
                self._sleep(delay=self._delay * 3) # longer pause before longer words
            for c in token:
                self._emit(c)
                self._sleep()


class TypioContext:
    """Read-only typing context passed to custom typing modes."""

    def __init__(self, printer: "_TypioPrinter") -> None:
        """
        Initialize the typing context.

        :param printer: printer
        """
        self._printer = printer

    def emit(self, text: str) -> None:
        """
        Emit a text fragment.

        :param text: text fragment to write
        """
        self._printer._emit(text)

    def flush(self) -> None:
        """Flush the underlying output stream."""
        self._printer.flush()

    def sleep(self, delay: Optional[float] = None, jitter: Optional[float] = None) -> None:
        """
        Sleep for a given delay with optional random jitter.

        :param delay: base delay (in seconds) between emitted units
        :param jitter: random jitter added/subtracted from delay
        """
        if delay is not None:
            if not isinstance(delay, (int, float)) or delay < 0:
                raise TypioError(INVALID_DELAY_ERROR)

        if jitter is not None:
            if not isinstance(jitter, (int, float)) or jitter < 0:
                raise TypioError(INVALID_JITTER_ERROR)

        self._printer._sleep(delay=delay, jitter=jitter)

    @property
    def delay(self) -> float:
        """Delay property."""
        return self._printer._delay

    @property
    def jitter(self) -> float:
        """Jitter property."""
        return self._printer._jitter


def type_print(
        text: str,
        *,
        delay: float = 0.04,
        jitter: float = 0,
        end: str = "\n",
        mode: Union[TypeMode, Callable] = TypeMode.CHAR,
        file: Optional[TextIOBase] = None) -> None:
    """
    Print text with typing effects.

    :param text: text to be printed
    :param delay: base delay (in seconds) between emitted units
    :param jitter: random jitter added/subtracted from delay
    :param end: ending character(s)
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
        mode: Union[TypeMode, Callable] = TypeMode.CHAR) -> Callable:
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
