# -*- coding: utf-8 -*-
"""typio params."""
from enum import Enum

TYPIO_VERSION = "0.1"


class TypeMode(Enum):
    CHAR = "char"
    WORD = "word"
    LINE = "line"
    SENTENCE = "sentence"
    TYPEWRITER = "typewriter"
    ADAPTIVE = "adaptive"