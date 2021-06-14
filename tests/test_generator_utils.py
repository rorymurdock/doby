"""Doby generator utils testing"""
from doby.generator import utils
from . import get_random


def test_get_description_empty():
    """Test get_description_empty"""
    assert utils.get_description({}) == ""


def test_get_description_key_description():
    """Test get_description_key_description"""
    description = get_random.text()
    assert utils.get_description({"description": description}) == description


def test_get_description_key_summary():
    """Test get_description_key_summary"""
    summary = get_random.text()
    assert utils.get_description({"summary": summary}) == summary
