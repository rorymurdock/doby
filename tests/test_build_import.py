"""Doby function testing"""
from doby.build import imports


def test_build_import():
    """Test build_imports"""

    config = {
        "requirements": {
            "apple": {},
            "orange": {"builtin": True, "operator": "==", "version": "1.0.0"},
            "pear": {"builtin": False, "operator": "==", "version": "1.0.0"},
            "lime": {"builtin": False, "operator": "=="},
        }
    }

    assert imports.build_import(config) == (
        ["apple", "pear==1.0.0", "lime"],
        [
            "import logging",
            "import reqrest",
            "import apple",
            "import orange",
            "import pear",
            "import lime",
            "",
        ],
    )
