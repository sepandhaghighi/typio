# -*- coding: utf-8 -*-
import pytest
from unittest.mock import patch
from typio import TypeMode
from typio.cli import main
from typio.params import TYPIO_VERSION, TYPIO_OVERVIEW
from typio.params import INVALID_NON_NEGATIVE_NUMBER_ERROR


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
            )


def test_custom_arguments():
    with patch(
        "sys.argv",
        [
            "typio",
            "--text", "Hello",
            "--delay", "0.1",
            "--jitter", "0.2",
            "--end", "!",
            "--mode", "word",
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


def test_invalid_mode(capsys):
    with patch("sys.argv", ["typio", "--mode", "invalid"]):
        with pytest.raises(SystemExit):
            main()

    _, err = capsys.readouterr()
    assert "invalid choice" in err.lower()
