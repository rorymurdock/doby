"""Doby README testing"""
import os
import argparse
import pytest
import mock
from doby import __main__, utils

args = argparse.Namespace(config="configs/api.json", output="exports", v=None)


def test_parse_args():
    """Test parse_args"""
    assert __main__.parse_args(
        ("configs/api.json", "exports", "-v")
    ) == argparse.Namespace(config="configs/api.json", output="exports", v=True)


def test_parse_args_no_debug():
    """Test parse_args_no_debug"""
    assert __main__.parse_args(("configs/api.json", "exports")) == argparse.Namespace(
        config="configs/api.json", output="exports", v=None
    )


def test_parse_args_missing_arg():
    """Test parse_args_missing_arg"""
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        __main__.parse_args(("configs/api.json"))

    assert pytest_wrapped_e.type == SystemExit


def test_main():
    """Test main"""
    assert (
        __main__.main(
            argparse.Namespace(config="configs/api.json", output="exports", v=None)
        )
        is True
    )
    assert os.path.isdir("exports") is True
    assert os.path.isdir("exports/PyTest") is True
    assert os.path.isfile("exports/PyTest/PyTest.py") is True
    assert os.path.isfile("exports/README.md") is True
    assert os.path.isfile("exports/requirements.txt") is True


def test_init():
    """Test init"""
    with mock.patch.object(__main__, "__name__", "__main__"):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            assert __main__.init() is True
        assert pytest_wrapped_e.type == SystemExit


def test_yapf():
    """Test yapf"""
    utils.clear_export_directory("exports/")
    utils.write_to_file("PyTest.py", "exports/", "def badpython")
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        __main__.yapf(args)

    assert pytest_wrapped_e.type == SystemExit


def test_black():
    """Test black"""
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        __main__.black(args, "PyTest")

    assert pytest_wrapped_e.type == SystemExit


def test_test_compile():
    """Test test_compile"""
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        __main__.test_compile(args, "PyTest")

    assert pytest_wrapped_e.type == SystemExit
