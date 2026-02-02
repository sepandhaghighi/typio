# -*- coding: utf-8 -*-
"""typio params."""
from enum import Enum

TYPIO_VERSION = "0.1"


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
INVALID_MODE_ERROR = "`mode` must be a TypeMode enum value."
INVALID_END_ERROR = "`end` must be a str."
INVALID_FILE_ERROR = "`file` must be a file-like object."
