# -*- coding: utf-8 -*-
import pytest
from unittest.mock import patch
from typio import TypeMode
from typio.cli import main
from typio.params import TYPIO_VERSION, TYPIO_OVERVIEW
from typio.params import INVALID_NON_NEGATIVE_NUMBER_ERROR, EXIT_MESSAGE


def test_version_flag(capsys):
    with patch("sys.argv", ["typio", "--version"]):
        main()
    out, _ = capsys.readouterr()
    assert out.strip() == TYPIO_VERSION


def test_default_execution():
    with patch("sys.argv", ["typio"]):
        with patch("typio.cli.type_print") as mock_type_print:
            main()
            mock_type_print.assert_called_once_with(
                text=TYPIO_OVERVIEW,
                delay=0.04,
                jitter=0.0,
                end="\n",
                mode=TypeMode.CHAR,
                seed=None,
            )


def test_custom_arguments():
    with patch(
        "sys.argv",
        [
            "typio",
            "Hello",
            "--delay", "0.1",
            "--jitter", "0.2",
            "--end", "!",
            "--mode", "word",
            "--seed", "123",
        ],
    ):
        with patch("typio.cli.type_print") as mock_type_print:
            main()
            mock_type_print.assert_called_once_with(
                text="Hello",
                delay=0.1,
                jitter=0.2,
                end="!",
                mode=TypeMode.WORD,
                seed=123,
            )


def test_custom_arguments_text_replacement():
    with patch(
        "sys.argv",
        [
            "typio",
            "Hello",
            "--text", "HelloWorld",
            "--delay", "0.1",
            "--jitter", "0.2",
            "--end", "!",
            "--mode", "word",
            "--seed", "123",
        ],
    ):
        with patch("typio.cli.type_print") as mock_type_print:
            main()
            mock_type_print.assert_called_once_with(
                text="HelloWorld",
                delay=0.1,
                jitter=0.2,
                end="!",
                mode=TypeMode.WORD,
                seed=123,
            )


def test_negative_delay(capsys):
    with patch("sys.argv", ["typio", "--delay", "-1"]):
        with pytest.raises(SystemExit):
            main()

    _, err = capsys.readouterr()
    assert INVALID_NON_NEGATIVE_NUMBER_ERROR.format(value="-1") in err


def test_wrong_delay(capsys):
    with patch("sys.argv", ["typio", "--delay", "abc"]):
        with pytest.raises(SystemExit):
            main()

    _, err = capsys.readouterr()
    assert INVALID_NON_NEGATIVE_NUMBER_ERROR.format(value="abc") in err


def test_negative_jitter(capsys):
    with patch("sys.argv", ["typio", "--jitter", "-1"]):
        with pytest.raises(SystemExit):
            main()

    _, err = capsys.readouterr()
    assert INVALID_NON_NEGATIVE_NUMBER_ERROR.format(value="-1") in err


def test_wrong_jitter(capsys):
    with patch("sys.argv", ["typio", "--jitter", "abc"]):
        with pytest.raises(SystemExit):
            main()

    _, err = capsys.readouterr()
    assert INVALID_NON_NEGATIVE_NUMBER_ERROR.format(value="abc") in err


def test_wrong_seed(capsys):
    with patch("sys.argv", ["typio", "--seed", "abc"]):
        with pytest.raises(SystemExit):
            main()

    _, err = capsys.readouterr()
    assert "invalid int value" in err.lower()


def test_invalid_mode(capsys):
    with patch("sys.argv", ["typio", "--mode", "invalid"]):
        with pytest.raises(SystemExit):
            main()

    _, err = capsys.readouterr()
    assert "invalid choice" in err.lower()


def test_keyboard_interrupt(capsys):
    with patch("typio.cli._parse_args", side_effect=KeyboardInterrupt):
        with pytest.raises(SystemExit):
            main()

    out, _ = capsys.readouterr()
    assert EXIT_MESSAGE in out


def test_eof_error(capsys):
    with patch("typio.cli._parse_args", side_effect=EOFError):
        with pytest.raises(SystemExit):
            main()

    out, _ = capsys.readouterr()
    assert EXIT_MESSAGE in out
