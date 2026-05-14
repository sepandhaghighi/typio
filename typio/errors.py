# -*- coding: utf-8 -*-
"""typio errors."""


class TypioError(Exception):
    """Base exception for all Typio errors."""

    pass


class TypioValidationError(TypioError, ValueError):
    """Base class for validation errors in Typio."""

    pass
