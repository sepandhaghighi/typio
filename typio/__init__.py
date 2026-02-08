# -*- coding: utf-8 -*-
"""typio modules."""
from .params import TYPIO_VERSION, TypeMode
from .errors import TypioError
from .functions import type_print, typestyle, TypioContext

__version__ = TYPIO_VERSION
__all__ = ["TypeMode", "TypioError", "type_print", "typestyle", "TypioContext"]
