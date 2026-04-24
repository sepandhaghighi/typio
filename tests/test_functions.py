# -*- coding: utf-8 -*-
import io
import sys
from unittest.mock import patch
from typio import type_print, typestyle
from typio import TypeMode
import random


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


def test_accelerate_mode():
    buffer = io.StringIO()
    text = "Hello, world!" * 100
    type_print(text, file=buffer, delay=0.01, mode=TypeMode.ACCELERATE)
    assert buffer.getvalue() == text + "\n"


def test_decelerate_mode():
    buffer = io.StringIO()
    text = "Hello, world!" * 100
    type_print(text, file=buffer, delay=0.01, mode=TypeMode.DECELERATE)
    assert buffer.getvalue() == text + "\n"


def test_burst_mode1():
    buffer = io.StringIO()
    text = "Hello, world!" * 100
    with patch("random.randint", return_value=5):
        type_print(text, file=buffer, delay=0.01, mode=TypeMode.BURST)
    assert buffer.getvalue() == text + "\n"


def test_burst_mode2():
    buffer = io.StringIO()
    text = "Hello, world!" * 100 + "X"
    with patch("random.randint", return_value=7):
        type_print(text, file=buffer, delay=0.01, mode=TypeMode.BURST)
    assert buffer.getvalue() == text + "\n"


def test_fat_finger_mode():
    random.seed(1)
    buffer = io.StringIO()
    text = "Hello, world!"
    type_print(text, file=buffer, delay=0.01, mode=TypeMode.FAT_FINGER)
    assert buffer.getvalue() == 'Hello, wo4l\x08 \x08\x08 \x084l\x08 \x08\x08 \x08rld~\n\x08 \x08\x08 \x08!\n'


def test_thoughtful_mode():
    buffer = io.StringIO()
    text = "Hello, myworld! How are you?"
    type_print(text, file=buffer, delay=0.01, mode=TypeMode.THOUGHTFUL)
    assert buffer.getvalue() == text + "\n"


def test_heartbeat_mode():
    buffer = io.StringIO()
    text = "Hello, myworld! How are you?"
    type_print(text, file=buffer, delay=0.01, mode=TypeMode.HEARTBEAT)
    assert buffer.getvalue() == text + "\n"


def test_rewind_mode():
    random.seed(1)
    buffer = io.StringIO()
    text = "Hello, world!" * 8
    type_print(text, file=buffer, delay=0.01, mode=TypeMode.REWIND)
    assert buffer.getvalue() == 'Hello, world!Hello, world!Hello, world!Hello, world!Hello, world!Hello, world!Hello, world!Hello, world!\x08 \x08\x08 \x08\x08 \x08\x08 \x08\x08 \x08\x08 \x08world!\n'


def test_glitch_mode():
    random.seed(1)
    buffer = io.StringIO()
    text = "Hello, world!" * 2
    type_print(text, file=buffer, delay=0.01, mode=TypeMode.GLITCH)
    assert buffer.getvalue() == 'Hello, wor&\x08 \x08ld!&\x08 \x08Hello,#\x08 \x08 worl@\x08 \x08d!\n'


def test_random_case_mode():
    random.seed(1)
    buffer = io.StringIO()
    text = "Hello, world!"
    type_print(text, file=buffer, delay=0.01, mode=TypeMode.RANDOM_CASE)
    assert buffer.getvalue() == 'HelLO, WorLD!\n'


def test_wave_mode():
    buffer = io.StringIO()
    text = "Hello, world!"
    type_print(text, file=buffer, delay=0.01, mode=TypeMode.WAVE)
    assert buffer.getvalue() == 'Hello, world!\n'


def test_stutter_mode():
    random.seed(1)
    buffer = io.StringIO()
    text = "Hello, world!" * 8
    type_print(text, file=buffer, delay=0.01, mode=TypeMode.STUTTER)
    assert buffer.getvalue() == 'Hello, world!Hello, world!Hello, world!Hello, world!Hello, world!Hello, world!Hello, world!Hello, w-world!\n'


def test_nervous_mode():
    buffer = io.StringIO()
    text = "Hello, world!"
    type_print(text, file=buffer, delay=0.01, mode=TypeMode.NERVOUS)
    assert buffer.getvalue() == 'Hello, world!\n'


def test_hesitation_mode():
    random.seed(1)
    buffer = io.StringIO()
    text = "Hello, world!" * 8
    type_print(text, file=buffer, delay=0.01, mode=TypeMode.HESITATION)
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
