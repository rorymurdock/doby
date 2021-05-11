"""Test Doby config"""
import os
import json
import logging
import pytest
from doby.config import walk, load_config
from . import get_random

TEST_ID = get_random.text(8).upper()


def test_walk_one_key():
    """Test one key merge"""

    config_dict = {}
    override_config_dict = {}

    config_dict["debug"] = False
    config_dict["debug"] = True

    assert walk(config=config_dict, override=override_config_dict) == {"debug": True}


def test_walk_no_matching_key():
    """Test no matching keys merge"""

    config_dict = {}
    override_config_dict = {}

    config_dict["debug"] = True

    assert walk(config=config_dict, override=override_config_dict) == {"debug": True}


def test_walk_empty_override():
    """Test one empty dict merge"""

    config_dict = {}
    override_config_dict = {}

    config_dict["debug"] = False

    assert walk(config=config_dict, override=override_config_dict) == {"debug": False}


def test_walk_nested_dicts():
    """Test nested dicts"""

    config_dict = {}
    override_config_dict = {}

    config_dict["debug"] = False
    config_dict["headers"] = {}
    config_dict["headers"]["nested"] = False

    override_config_dict["debug"] = False
    override_config_dict["headers"] = {}
    override_config_dict["headers"]["nested"] = True

    assert walk(config=config_dict, override=override_config_dict) == {
        "debug": False,
        "headers": {"nested": True},
    }


def test_walk_not_matching_nested_dicts():
    """Test non matching dicts"""

    config_dict = {}
    override_config_dict = {}

    config_dict["debug"] = False

    override_config_dict["debug"] = True
    override_config_dict["headers"] = {}
    override_config_dict["headers"]["nested"] = False

    assert walk(config_dict, override_config_dict) == {
        "debug": True,
        "headers": {"nested": False},
    }


def test_load_config():
    """Test loading config"""

    write_config(create_test_config())
    assert load_config(f"doby_config_test_{TEST_ID}.json") == {
        "debug": True,
        "description": "PyTest configuration library",
        "functions": {},
        "headers": {},
        "name": "fruitTest",
        "override": False,
        "hostname": 'self.auth["url"]',
    }


def test_load_config_bad_filename(caplog):
    """Test loading a file that doesn't exist"""

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        load_config("bad_file.json")

    assert pytest_wrapped_e.type == SystemExit
    assert caplog.records[3].levelname == "CRITICAL"
    assert caplog.records[3].message == "File bad_file.json doesn't exist, exiting"


def test_load_config_bad_json_file(caplog):
    """Test loading a file that isn't JSON"""

    with open("bad_file.txt", "w") as text_file:
        text_file.write("Delete me, pytest only")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        load_config("bad_file.txt")

    assert pytest_wrapped_e.type == SystemExit
    assert caplog.records[3].levelname == "CRITICAL"
    assert (
        caplog.records[3].message
        == "Unable to parse JSON config file: Expecting value: line 1 column 1 (char 0)"
    )

    os.remove("bad_file.txt")


def test_load_config_override():
    """Test loading config with an override"""

    override_config = create_test_config()
    override_config["name"] = "PyTest override configuration"

    write_config(create_test_config())
    assert load_config(f"doby_config_test_{TEST_ID}.json") == {
        "debug": True,
        "description": "PyTest configuration library",
        "functions": {},
        "headers": {},
        "name": "fruitTest",
        "override": False,
        "hostname": 'self.auth["url"]',
    }

    write_config(
        override_config,
        f"doby_config_test_{TEST_ID}_override.json",
    )

    assert load_config(f"doby_config_test_{TEST_ID}.json") == {
        "debug": True,
        "description": "PyTest configuration library",
        "functions": {},
        "headers": {},
        "name": "PyTest override configuration",
        "hostname": 'self.auth["url"]',
    }


def create_test_config():
    """Create a test config file"""

    config = {}

    # Add name & description
    config["name"] = "fruitTest"
    config["description"] = "PyTest configuration library"

    # Add url
    config["hostname"] = 'self.auth["url"]'

    # Add requirements
    config["debug"] = True

    # Add header
    config["headers"] = {}

    # Add function
    config["functions"] = {}

    return config


def write_config(config, filename=None):
    """Write the config to file"""

    if filename is None:
        filename = f"doby_config_test_{TEST_ID}.json"

    logging.info("Writing config to file")
    with open(filename, "w", encoding="utf8") as output:
        json.dump(config, output, indent=4)

    return filename


def create_test_all_config():
    """Create a test config file with enough config to make a library"""

    config = {
        "name": "PyTest",
        "description": "PyTest configuration library",
        "debug": True,
        "hostname": {
            "static": "cn135.awmdm.com",
            "variable": "url",
            "function": "get_url()",
        },
        "headers": {
            "rest": {
                "Accept": {"static": "application/json"},
                "api-key": {"function": "get_api_key()"},
            }
        },
        "functions": {
            "custom": {
                "custom_test": {
                    "name": "custom_test",
                    "description": "Custom test description",
                    "parameters": {
                        "pagesize": {
                            "description": "How many results to return",
                            "type": "int",
                            "defaultValue": "500",
                        }
                    },
                    "code": {},
                }
            },
            "init": {
                "description": "This is called when the class is initialised",
                "parameters": {
                    "debug": {
                        "description": "Enables debugging",
                        "type": "bool",
                        "defaultValue": "False",
                    }
                },
                "code": [],
            },
            "main": {
                "run": True,
                "description": "This is the main function",
                "code": ["uem = WSO()", 'print(uem.systemInfo()["ProductVersion"])'],
            },
            "endpoint": {
                "systemInfo": {
                    "category": "SystemAPIs",
                    "name": "systemInfo",
                    "description": "Gets System information",
                    "method": "get",
                    "path": "/api/system/info",
                    "response": "response.txt",
                    "header": "rest",
                    "returns": "response.text",
                    "checkHttpResponse": True,
                    "payload": {
                        "pagesize": {"static": 500},
                        "page": {"variable": "page"},
                        "apikey": {"function": "get_api_key()"},
                    },
                    "parameters": {
                        "pagesize": {
                            "description": "How many results to return",
                            "type": "int",
                            "defaultValue": "500",
                        },
                        "page": {
                            "description": "Which page of results to return",
                            "type": "int",
                            "defaultValue": "0",
                        },
                    },
                    "code": {"start": [], "mid": [], "end": []},
                    "querystring": {
                        "pagesize": {"static": 500},
                        "page": {"variable": "page"},
                        "apikey": {"function": "get_api_key()"},
                    },
                }
            },
        },
        "requirements": {
            "os": {"builtin": True, "operator": "==", "version": "1.0.0"},
            "reqrest": {},
            "panda": {"builtin": False, "operator": "==", "version": "1.0.0"},
        },
        ".gitignore": ["*.pyc"],
        "setup": {
            "version": "1.0.0",
            "author": "Me",
            "author_email": "me@example.com",
            "url": "https://example.com",
        },
    }

    return config
