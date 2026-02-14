# -*- coding: utf-8 -*-
"""typio params."""
from enum import Enum

TYPIO_VERSION = "0.3"

TYPIO_OVERVIEW = '''Typio is a lightweight Python library that prints text to the terminal as if it were being typed by a human.
It supports multiple typing modes (character, word, line, sentence, typewriter, and adaptive), configurable delays
and jitter for natural variation, and seamless integration with existing code via a simple function or a decorator.
Typio is designed to be minimal, extensible, and safe, making it ideal for demos, CLIs, tutorials, and storytelling in the terminal.

GitHub Repo: https://github.com/sepandhaghighi/typio'''


class TypeMode(Enum):
    """Type mode enum."""

    CHAR = "char"
    WORD = "word"
    LINE = "line"
    SENTENCE = "sentence"
    TYPEWRITER = "typewriter"
    ADAPTIVE = "adaptive"


INVALID_TEXT_ERROR = "`text` must be str or bytes."
INVALID_BYTE_ERROR = "bytes text must be UTF-8 decodable."
INVALID_DELAY_ERROR = "`delay` must be a non-negative number."
INVALID_JITTER_ERROR = "`jitter` must be a non-negative number."
INVALID_MODE_ERROR = "`mode` must be a TypeMode enum value or a callable custom mode."
INVALID_END_ERROR = "`end` must be a str."
INVALID_FILE_ERROR = "`file` must be a file-like object."
INVALID_NON_NEGATIVE_NUMBER_ERROR = "invalid non-negative number: '{value}'"
