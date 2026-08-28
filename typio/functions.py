# -*- coding: utf-8 -*-
"""typio functions."""

import sys
import time
import random
import re
import math
from functools import wraps
from io import TextIOBase
from typing import Any, Callable, Optional, Union, List
from .params import TypeMode, KEY_NEIGHBORS, GLITCH_CHARS
from .params import INVALID_TEXT_ERROR, INVALID_BYTE_ERROR, INVALID_DELAY_ERROR
from .params import INVALID_JITTER_ERROR, INVALID_MODE_ERROR, INVALID_FILE_ERROR
from .params import INVALID_END_ERROR, INVALID_SEED_ERROR
from .errors import TypioValidationError


def _validate(
    text: Any,
    delay: Any,
    jitter: Any,
    mode: Any,
    end: Any,
    file: Any,
    seed: Any,
) -> str:
    """
    Validate and normalize inputs for typing operations.

    :param text: text to be printed
    :param delay: base delay (in seconds) between emitted units
    :param jitter: random jitter added/subtracted from delay
    :param mode: typing mode controlling emission granularity
    :param end: ending character(s)
    :param file: output stream supporting a write() method
    :param seed: random seed for reproducibility
    """
    if not isinstance(text, (str, bytes)):
        raise TypioValidationError(INVALID_TEXT_ERROR)

    if isinstance(text, bytes):
        try:
            text = text.decode()
        except Exception:
            raise TypioValidationError(INVALID_BYTE_ERROR)

    if not isinstance(delay, (int, float)) or delay < 0:
        raise TypioValidationError(INVALID_DELAY_ERROR)

    if not isinstance(jitter, (int, float)) or jitter < 0:
        raise TypioValidationError(INVALID_JITTER_ERROR)

    if not isinstance(mode, TypeMode) and not callable(mode):
        raise TypioValidationError(INVALID_MODE_ERROR)

    if not isinstance(end, str):
        raise TypioValidationError(INVALID_END_ERROR)

    if file is not None and not hasattr(file, "write"):
        raise TypioValidationError(INVALID_FILE_ERROR)

    if seed is not None and not isinstance(seed, int):
        raise TypioValidationError(INVALID_SEED_ERROR)
    text = f"{text}{end}"
    return text


class _TypioPrinter:
    """File-like object that emits text with typing effects."""

    def __init__(
            self,
            *,
            delay: float,
            jitter: float,
            mode: Union[TypeMode, Callable],
            out: TextIOBase,
            seed: Optional[int] = None) -> None:
        """
        Initialize the typing printer.

        :param delay: base delay (in seconds) between emitted units
        :param jitter: random jitter added/subtracted from delay
        :param mode: typing mode controlling emission granularity
        :param out: underlying output stream
        :param seed: random seed for reproducibility
        """
        self._delay = delay
        self._jitter = jitter
        self._mode = mode
        self._out = out
        self._random = random.Random(seed)

    def write(self, text: str) -> int:
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
        return len(text)

    def flush(self) -> None:
        """Flush the underlying output stream."""
        self._out.flush()

    @staticmethod
    def _split_tokens(text: str) -> List[str]:
        """
        Split text into tokens.

        :param text: text to be split into tokens
        """
        return re.findall(r"\S+|\s+", text)

    def _sleep(self, delay: Optional[float] = None, jitter: Optional[float] = None) -> None:
        """
        Sleep for a given delay with optional random jitter.

        :param delay: base delay (in seconds) between emitted units
        :param jitter: random jitter added/subtracted from delay
        """
        delay_ = self._delay if delay is None else delay
        jitter_ = self._jitter if jitter is None else jitter
        if delay_ <= 0:
            return
        if jitter_:
            delay_ += self._random.uniform(-jitter_, jitter_)
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
        for w in self._split_tokens(text):
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
                self._sleep(delay=self._delay * 4)

    def _mode_typewriter(self, text: str) -> None:
        """
        Emit text character by character with longer pauses after newlines.

        :param text: text to emit
        """
        for c in text:
            self._emit(c)
            self._sleep()
            if c == "\n":
                self._sleep(delay=self._delay * 5)

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
        burst_size = self._random.randint(3, 8)
        for c in text:
            buffer.append(c)
            if len(buffer) >= burst_size:
                self._emit("".join(buffer))
                buffer.clear()
                self._sleep()
                burst_size = self._random.randint(3, 8)
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
            if char in KEY_NEIGHBORS and self._random.random() < 0.03:
                wrong_char = self._random.choice(KEY_NEIGHBORS[char])
                self._emit(wrong_char)
                self._sleep(delay=self._delay * 1.25)
                extra_chars = []
                decay_rate = 0.6
                current_j = i + 1
                while current_j < len(text) and self._random.random() < (decay_rate ** (len(extra_chars) + 1)):
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
        for token in self._split_tokens(text):
            if token.strip() and len(token.strip()) > 6:
                self._sleep(delay=self._delay * 3)
            for c in token:
                self._emit(c)
                self._sleep()

    def _mode_heartbeat(self, text: str) -> None:
        """
        Emit text with alternating short and long pauses to simulate a heartbeat-like rhythm.

        :param text: text to emit
        """
        toggle = True
        for c in text:
            self._emit(c)
            if toggle:
                self._sleep(delay=self._delay * 0.5)
            else:
                self._sleep(delay=self._delay * 1.8)
            toggle = not toggle

    def _mode_rewind(self, text: str) -> None:
        """
        Emit text while occasionally deleting and retyping words to simulate reconsideration.

        :param text: text to emit
        """
        words = self._split_tokens(text)
        for word in words:
            for c in word:
                self._emit(c)
                self._sleep()
            if word.strip() and self._random.random() < 0.1:
                self._sleep(delay=self._delay * 3)
                for _ in word:
                    self._emit("\b \b")
                    self._sleep(delay=self._delay * 0.5)
                self._sleep()
                for c in word:
                    self._emit(c)
                    self._sleep()

    def _mode_glitch(self, text: str) -> None:
        """
        Emit text with occasional random glitches that are quickly corrected.

        :param text: text to emit
        """
        for c in text:
            self._emit(c)
            self._sleep()
            if self._random.random() < 0.05:
                glitch = self._random.choice(GLITCH_CHARS)
                self._emit(glitch)
                self._sleep(delay=self._delay * 2)
                self._emit("\b \b")
                self._sleep()

    def _mode_random_case(self, text: str) -> None:
        """
        Emit text with randomly varying character casing.

        :param text: text to emit
        """
        for c in text:
            if c.isalpha():
                c = c.upper() if self._random.random() < 0.5 else c.lower()
            self._emit(c)
            self._sleep()

    def _mode_wave(self, text: str) -> None:
        """
        Emit text with sinusoidal delay variation.

        :param text: text to emit
        """
        wave_2pif, wave_len, wave_bias = 0.3, 0.5, 0.4
        for i, c in enumerate(text):
            factor = wave_bias + wave_len * (1 + math.sin(i * wave_2pif))
            self._emit(c)
            self._sleep(delay=self._delay * factor)

    def _mode_stutter(self, text: str) -> None:
        """
        Emit text with stuttering effect on some words.

        :param text: text to emit
        """
        words = self._split_tokens(text)
        for word in words:
            for i, c in enumerate(word):
                if c.isalpha() and i == 0 and self._random.random() < 0.1:
                    repeat = self._random.randint(1, 2)
                    for _ in range(repeat):
                        self._emit(c + "-")
                        self._sleep(delay=self._delay * 1.2)
                self._emit(c)
                self._sleep()

    def _mode_nervous(self, text: str) -> None:
        """
        Emit text erratically typing with inconsistent pauses.

        :param text: text to emit
        """
        for c in text:
            self._emit(c)
            factor = 2 ** self._random.uniform(-2, 2)
            self._sleep(delay=self._delay * factor)

    def _mode_hesitation(self, text: str) -> None:
        """
        Emit text with occasional pauses within words to simulate human hesitation.

        :param text: text to emit
        """
        words = self._split_tokens(text)
        for word in words:
            for c in word:
                self._emit(c)
                if c.isalpha() and self._random.random() < 0.08:
                    factor = self._random.uniform(2, 5)
                    self._sleep(delay=self._delay * factor)
                else:
                    self._sleep()

    def _mode_overthink(self, text: str) -> None:
        """
        Emit text while occasionally deleting and retyping a chunk of text to simulate overthinking.

        :param text: text to emit
        """
        words = self._split_tokens(text)
        for word in words:
            i = 0
            while i < len(word):
                c = word[i]
                self._emit(c)
                self._sleep()

                if i > 2 and self._random.random() < 0.15:
                    delete_count = self._random.randint(1, i // 2)
                    for _ in range(delete_count):
                        self._emit("\b \b")
                        self._sleep(delay=self._delay * 0.6)
                    i -= delete_count
                    self._sleep(delay=self._delay * 2)
                i += 1

    def _mode_confident(self, text: str) -> None:
        """
        Emit text quickly with brief pauses, adding longer delays after punctuation to simulate confident typing.

        :param text: text to emit
        """
        for c in text:
            self._emit(c)
            if c in ".!?":
                self._sleep(delay=self._delay * 5)
            elif c in ",;:":
                self._sleep(delay=self._delay * 2)
            else:
                self._sleep()

    def _mode_echo(self, text: str) -> None:
        """
        Emit text with occasional repetition of characters faintly, like a glitchy terminal echo.

        :param text: text to emit
        """
        for c in text:
            self._emit(c)
            self._sleep()
            if self._random.random() < 0.1 and c.strip():
                self._emit(c)
                self._sleep(delay=self._delay * 0.1)

    def _mode_drunk(self, text: str) -> None:
        """
        Emit text with erratic timing and occasional character duplication or skipping.

        :param text: text to emit
        """
        i = 0
        while i < len(text):
            c = text[i]

            if self._random.random() < 0.02:
                i += 1
                continue

            self._emit(c)

            if c.isalpha() and self._random.random() < 0.08:
                self._emit(c)
                self._sleep(delay=self._delay * 0.5)

            factor = self._random.uniform(0.3, 2.5)
            self._sleep(delay=self._delay * factor)

            i += 1

    def _mode_glide(self, text: str) -> None:
        """
        Emit text with smooth deceleration then acceleration.

        :param text: text to emit
        """
        total = len(text)

        for i, c in enumerate(text):
            self._emit(c)
            x = i / max(1, total - 1)
            t = 2 * (4 * x * (1 - x)) - 1
            factor = 2 ** t
            self._sleep(delay=self._delay * factor)

    def _mode_focus_drift(self, text: str) -> None:
        """
        Emit text with occasional attention drift, causing slowdowns and pauses mid-word.

        :param text: text to emit
        """
        for c in text:
            self._emit(c)
            self._sleep()
            if c.isalpha() and self._random.random() < 0.05:
                drift_length = self._random.randint(1, 4)
                factor = drift_length * self._random.uniform(1.5, 4)
                self._sleep(delay=self._delay * factor)

    def _mode_rubber_duck(self, text: str) -> None:
        """
        Emit text while occasionally repeating fragments as if explaining thoughts aloud to a rubber duck.

        :param text: text to emit
        """
        words = self._split_tokens(text)

        for word in words:
            for c in word:
                self._emit(c)
                self._sleep()
            stripped = word.strip()
            if (stripped and len(stripped) > 3 and self._random.random() < 0.12):
                self._sleep(delay=self._delay * 2)
                style = self._random.choice([
                    "full",
                    "thinking",
                ])
                if style == "full":
                    repeat = f"... {stripped}..."
                    for c in repeat:
                        self._emit(c)
                        self._sleep()
                else:
                    thinking = self._random.choice([
                        "... wait ...",
                        "... hmm ...",
                        "... actually ...",
                        "... okay ...",
                    ])
                    for c in thinking:
                        self._emit(c)
                        self._sleep()
                    for c in f" {stripped}...":
                        self._emit(c)
                        self._sleep()

    def _mode_panic(self, text: str) -> None:
        """
        Emit text with an increasing rate of typos and slower typing speed to simulate panicking.

        :param text: text to emit
        """
        total = max(1, len(text))

        for i, c in enumerate(text):
            stress = i / total
            if c.isalpha() and self._random.random() < (0.02 + stress * 0.25):
                wrong = self._random.choice(KEY_NEIGHBORS.get(c.lower(), [c]))
                self._emit(wrong)
                self._sleep(delay=self._delay * (1 + stress * 3))
                self._emit("\b \b")
                self._sleep(delay=self._delay * (1 + stress * 3))
            self._emit(c)
            if c in ".!?" and self._random.random() < stress * 0.4:
                self._emit(self._random.choice(["!", "?", "!!"]))

            factor = self._random.uniform(0.5, 1.5 + stress * 2)
            self._sleep(delay=self._delay * factor)


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
                raise TypioValidationError(INVALID_DELAY_ERROR)

        if jitter is not None:
            if not isinstance(jitter, (int, float)) or jitter < 0:
                raise TypioValidationError(INVALID_JITTER_ERROR)

        self._printer._sleep(delay=delay, jitter=jitter)

    @property
    def delay(self) -> float:
        """Delay property."""
        return self._printer._delay

    @property
    def jitter(self) -> float:
        """Jitter property."""
        return self._printer._jitter
    
    @property
    def random(self) -> random.Random:
        """Random number generator for the current typing operation."""
        return self._printer._random


def type_print(
        text: str,
        *,
        delay: float = 0.04,
        jitter: float = 0,
        end: str = "\n",
        mode: Union[TypeMode, Callable] = TypeMode.CHAR,
        seed: Optional[int] = None,
        file: Optional[TextIOBase] = None) -> None:
    """
    Print text with typing effects.

    :param text: text to be printed
    :param delay: base delay (in seconds) between emitted units
    :param jitter: random jitter added/subtracted from delay
    :param end: ending character(s)
    :param mode: typing mode controlling emission granularity
    :param seed: random seed for reproducibility
    :param file: output stream supporting a write() method
    """
    text = _validate(text, delay, jitter, mode, end, file, seed)
    out = file or sys.stdout

    printer = _TypioPrinter(
        delay=delay,
        jitter=jitter,
        mode=mode,
        out=out,
        seed=seed,
    )
    printer.write(text)
    printer.flush()


def typestyle(
        *,
        delay: float = 0.04,
        jitter: float = 0,
        seed: Optional[int] = None,
        mode: Union[TypeMode, Callable] = TypeMode.CHAR) -> Callable:
    """
    Apply typing effects to all print() calls inside the decorated function.

    :param delay: base delay (in seconds) between emitted units
    :param jitter: random jitter added/subtracted from delay
    :param seed: random seed for reproducibility
    :param mode: typing mode controlling emission granularity
    """
    _validate("", delay, jitter, mode, "", sys.stdout, seed)

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
                    seed=seed,
                )
                return func(*args, **kwargs)
            finally:
                sys.stdout = old_stdout

        return wrapper

    return decorator
