# -*- coding: utf-8 -*-
"""typio params."""
from enum import Enum

TYPIO_VERSION = "0.6"

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
    ACCELERATE = "accelerate"
    DECELERATE = "decelerate"
    BURST = "burst"
    FAT_FINGER = "fat-finger"
    THOUGHTFUL = "thoughtful"
    HEARTBEAT = "heartbeat"


EXIT_MESSAGE = "See you. Bye!"
INVALID_TEXT_ERROR = "`text` must be str or bytes."
INVALID_BYTE_ERROR = "bytes text must be UTF-8 decodable."
INVALID_DELAY_ERROR = "`delay` must be a non-negative number."
INVALID_JITTER_ERROR = "`jitter` must be a non-negative number."
INVALID_MODE_ERROR = "`mode` must be a TypeMode enum value or a callable custom mode."
INVALID_END_ERROR = "`end` must be a str."
INVALID_FILE_ERROR = "`file` must be a file-like object."
INVALID_NON_NEGATIVE_NUMBER_ERROR = "invalid non-negative number: '{value}'"

KEY_NEIGHBORS = {
    'q': 'wa12', 'w': 'qes23', 'e': 'wrd34', 'r': 'etf45', 't': 'ryg56', 'y': 'tuh67', 
    'u': 'yij78', 'i': 'uok89', 'o': 'ipl90', 'p': 'ol0-[;', '[': 'p;\']-=', ']': '[\'=\\\n',
    'a': 'qsz', 's': 'awdxz', 'd': 'serfcx', 'f': 'drtgvc', 'g': 'ftyhbv', 'h': 'gyujnb', 'j': 'huikmn', 
    'k': 'jiolm', 'l': 'kop;,.', ';': 'lp\'./', '\'': ';/[\n', 'z': 'asx ', 'x': 'zsdc ', 'c': 'xdfv ', 
    'v': 'cfgb ', 'b': 'vghn ', 'n': 'bhjm ', 'm': 'njk, ', ',': 'mkl. ', '.': ',l;\'/', '/': '.;\'',

    'Q': 'WA!@', 'W': 'QES@#', 'E': 'WRD#$', 'R': 'ETF$%', 'T': 'RYG%^', 'Y': 'TUH^&', 
    'U': 'YIJ&*', 'I': 'UOK*(', 'O': 'IPL()', 'P': 'OL)_+', '{': 'P:\"_+}', '}': '{+|\"',
    'A': 'QSZ', 'S': 'AWDXZ', 'D': 'SERFCX', 'F': 'DRTGVC', 'G': 'FTYHBV', 'H': 'GYUJNB', 
    'J': 'HUIKMN', 'K': 'JIOLM', 'L': 'KOP:<', ':': 'LP\">?', '\"': ':?{\n', 
    'Z': 'ASX ', 'X': 'ZSDC ', 'C': 'XDFV ', 'V': 'CFGB ', 'B': 'VGHN ', 'N': 'BHJM ', 
    'M': 'NJK< ', '<': 'MKL> ', '>': '<L:\"?', '?': '>:\";',

    '1': 'q2`', '2': '13qw', '3': '24we', '4': '35er', '5': '46rt', '6': '57ty',
    '7': '68yu', '8': '79ui', '9': '80io', '0': '9-op', '-': '0=p[', '=': '-][',

    '!': 'Q@~', '@': '!#QW', '#': '@$WE', '$': '#%ER', '%': '$^RT', '^': '%&TY',
    '&': '^*YU', '*': '&(UI', '(': '*)IO', ')': '(_OP', '_': ')+P{', '+': '_}{',
    
    ' ': 'cvbnm,./',
    '\n': 'lp;\'[]\\'
}
