# -*- coding: utf-8 -*-
import io
import sys
import unittest

import pytest

from typio import type_print, typestyle
from typio import TypeMode


def test_basic_print():
    buffer = io.StringIO()
    type_print("hello", file=buffer, delay=0)
    unittest.TestCase().assertEqual(buffer.getvalue(), "hello")


def test_bytes_input():
    buffer = io.StringIO()
    type_print(b"hello", file=buffer, delay=0)
    unittest.TestCase().assertEqual(buffer.getvalue(), "hello")


def test_word_mode():
    buffer = io.StringIO()
    type_print("hello world", file=buffer, delay=0, mode=TypeMode.WORD)
    unittest.TestCase().assertEqual(buffer.getvalue(), "hello world")


def test_line_mode():
    buffer = io.StringIO()
    text = "a\nb\nc\n"
    type_print(text, file=buffer, delay=0, mode=TypeMode.LINE)
    unittest.TestCase().assertEqual(buffer.getvalue(), text)


def test_sentence_mode():
    buffer = io.StringIO()
    text = "Hello! How are you?"
    type_print(text, file=buffer, delay=0, mode=TypeMode.SENTENCE)
    unittest.TestCase().assertEqual(buffer.getvalue(), text)


def test_typewriter_mode():
    buffer = io.StringIO()
    text = "Hello\nWorld\n"
    type_print(text, file=buffer, delay=0, mode=TypeMode.TYPEWRITER)
    unittest.TestCase().assertEqual(buffer.getvalue(), text)


def test_adaptive_mode():
    buffer = io.StringIO()
    text = "Hello, world!"
    type_print(text, file=buffer, delay=0, mode=TypeMode.ADAPTIVE)
    unittest.TestCase().assertEqual(buffer.getvalue(), text)


def test_default_stdout_capture(capsys):
    type_print("hello", delay=0)
    captured = capsys.readouterr()
    assert captured.out == "hello"


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
