# -*- coding: utf-8 -*-
import pytest

from typio import type_print, typestyle
from typio.errors import TypioError


def test_invalid_text_type():
    with pytest.raises(TypioError):
        type_print(123, delay=0)


def test_invalid_bytes():
    with pytest.raises(TypioError):
        type_print(b"\xff\xff", delay=0)


def test_negative_delay():
    with pytest.raises(TypioError):
        type_print("test", delay=-1)


def test_invalid_delay_type():
    with pytest.raises(TypioError):
        type_print("test", delay="fast")


def test_negative_jitter():
    with pytest.raises(TypioError):
        type_print("test", jitter=-0.1)


def test_invalid_jitter_type():
    with pytest.raises(TypioError):
        type_print("test", jitter="nope")


def test_invalid_mode():
    with pytest.raises(TypioError):
        type_print("test", mode="char")


def test_invalid_file():
    with pytest.raises(TypioError):
        type_print("test", file=123)


def test_typestyle_invalid_mode():
    with pytest.raises(TypioError):
        typestyle(mode="char")


def test_typestyle_invalid_delay():
    with pytest.raises(TypioError):
        typestyle(delay=-1)


def test_typestyle_invalid_jitter():
    with pytest.raises(TypioError):
        typestyle(jitter=-0.5)
