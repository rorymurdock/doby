"""Tidy up test files"""
import re
import os
import logging
from doby.utils import clear_export_directory


def test_cleanup():
    """Delete config files generated during tests"""

    for file in os.listdir("."):
        if re.search("doby_config_test_", file):
            logging.warning("Deleting %s", file)
            os.remove(file)

    clear_export_directory("exports/")

    assert True
