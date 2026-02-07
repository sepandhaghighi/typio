# -*- coding: utf-8 -*-
import pytest

from typio import type_print, typestyle
from typio import TypioError


def test_invalid_text_type():
    with pytest.raises(TypioError, match=r"`text` must be str or bytes."):
        type_print(123, delay=0)


def test_invalid_bytes():
    with pytest.raises(TypioError, match=r"bytes text must be UTF-8 decodable."):
        type_print(b"\xff\xff", delay=0)


def test_negative_delay():
    with pytest.raises(TypioError, match=r"`delay` must be a non-negative number."):
        type_print("test", delay=-1)


def test_invalid_delay_type():
    with pytest.raises(TypioError, match=r"`delay` must be a non-negative number."):
        type_print("test", delay="fast")


def test_negative_jitter():
    with pytest.raises(TypioError, match=r"`jitter` must be a non-negative number."):
        type_print("test", jitter=-0.1)


def test_invalid_jitter_type():
    with pytest.raises(TypioError, match=r"`jitter` must be a non-negative number."):
        type_print("test", jitter="nope")


def test_invalid_mode():
    with pytest.raises(TypioError, match=r"`mode` must be a TypeMode enum value."):
        type_print("test", mode="char")


def test_invalid_end():
    with pytest.raises(TypioError, match=r"`end` must be a str."):
        type_print("test", end=1)


def test_invalid_file():
    with pytest.raises(TypioError, match=r"`file` must be a file-like object."):
        type_print("test", file=123)


def test_typestyle_invalid_mode():
    with pytest.raises(TypioError, match=r"`mode` must be a TypeMode enum value."):
        typestyle(mode="char")


def test_typestyle_invalid_delay():
    with pytest.raises(TypioError, match=r"`delay` must be a non-negative number."):
        typestyle(delay=-1)


def test_typestyle_invalid_jitter():
    with pytest.raises(TypioError, match=r"`jitter` must be a non-negative number."):
        typestyle(jitter=-0.5)


def test_typiocontext_sleep_invalid_delay():
    buffer = io.StringIO()
    def custom(ctx: TypioContext, text: str):
        ctx.sleep(delay=-1)
    with pytest.raises(TypioError, match=r"`delay` must be a non-negative number."):
        type_print("x", file=buffer, delay=0, mode=custom)


def test_typiocontext_sleep_invalid_jitter():
    buffer = io.StringIO()
    def custom(ctx: TypioContext, text: str):
        ctx.sleep(jitter=-0.5)
    with pytest.raises(TypioError, match=r"`jitter` must be a non-negative number."):
        type_print("x", file=buffer, delay=0, mode=custom)


