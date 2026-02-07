# -*- coding: utf-8 -*-
import io
import sys

from typio import type_print, typestyle
from typio import TypeMode


def test_basic_print():
    buffer = io.StringIO()
    type_print("hello", file=buffer, delay=0)
    assert buffer.getvalue() == "hello\n"


def test_end():
    buffer = io.StringIO()
    type_print("hello", file=buffer, delay=0, end="\nqw")
    assert buffer.getvalue() == "hello\nqw"


def test_bytes_input():
    buffer = io.StringIO()
    type_print(b"hello", file=buffer, delay=0)
    assert buffer.getvalue() == "hello\n"


def test_word_mode():
    buffer = io.StringIO()
    type_print("hello world", file=buffer, delay=0, mode=TypeMode.WORD)
    assert buffer.getvalue() == "hello world\n"


def test_line_mode():
    buffer = io.StringIO()
    text = "a\nb\nc\n"
    type_print(text, file=buffer, delay=0, mode=TypeMode.LINE)
    assert buffer.getvalue() == text + "\n"


def test_sentence_mode():
    buffer = io.StringIO()
    text = "Hello! How are you?"
    type_print(text, file=buffer, delay=1, jitter=0, mode=TypeMode.SENTENCE)
    assert buffer.getvalue() == text + "\n"


def test_typewriter_mode():
    buffer = io.StringIO()
    text = "Hello\nWorld\n"
    type_print(text, file=buffer, delay=1, jitter=0.05, mode=TypeMode.TYPEWRITER)
    assert buffer.getvalue() == text + "\n"


def test_adaptive_mode():
    buffer = io.StringIO()
    text = "Hello, world!"
    type_print(text, file=buffer, delay=0, mode=TypeMode.ADAPTIVE)
    assert buffer.getvalue() == text + "\n"


def test_default_stdout_capture(capsys):
    type_print("hello", delay=0)
    captured = capsys.readouterr()
    assert captured.out == "hello\n"


def test_typiocontext_emit():
    buffer = io.StringIO()

    def custom(ctx, text):
        ctx.emit(text)
    type_print("hello", file=buffer, delay=0, mode=custom)
    assert buffer.getvalue() == "hello\n"


def test_typiocontext_delay_and_jitter_access():
    buffer = io.StringIO()

    def custom(ctx, text):
        assert ctx.delay == 0.1
        assert ctx.jitter == 0.2
        ctx.emit(text)
    type_print(
        "hello",
        file=buffer,
        delay=0.1,
        jitter=0.2,
        mode=custom,
    )
    assert buffer.getvalue() == "hello\n"


def test_typiocontext_flush():
    buffer = io.StringIO()

    def custom(ctx, text):
        ctx.emit("hello")
        ctx.sleep()
        ctx.flush()
    type_print("ignored", file=buffer, delay=0, mode=custom)
    assert buffer.getvalue() == "hello"


def test_typiocontext_sleep_override():
    buffer = io.StringIO()

    def custom(ctx, text):
        ctx.emit("A")
        ctx.sleep(delay=0.05, jitter=0.02)
        ctx.emit("B")
    type_print("X", file=buffer, delay=0.1, mode=custom)
    assert buffer.getvalue() == "AB"


def test_typestyle_decorator():
    buffer = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buffer

    @typestyle(delay=0, mode=TypeMode.CHAR)
    def demo():
        print("hello")
        print("world")

    try:
        demo()
    finally:
        sys.stdout = old_stdout

    assert buffer.getvalue() == "hello\nworld\n"


def test_typestyle_return_value():
    @typestyle(delay=0)
    def func():
        print("x")
        return 42

    assert func() == 42


def test_typiocontext_with_typestyle(capsys):
    def custom(ctx, text):
        ctx.emit(text.upper())

    @typestyle(delay=0, mode=custom)
    def demo():
        print("hello")
        print("world")

    demo()
    captured = capsys.readouterr()
    assert captured.out == "HELLO\nWORLD\n"
