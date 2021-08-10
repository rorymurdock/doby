"""Doby util testing"""
import os
import glob
import shutil

# from doby import utils
from doby.utils import (
    key_exists,
    get_debug,
    write_to_file,
    write_list_to_file,
    indent,
    get_parameters,
    generate_dictionary_variable_types,
    get_variable_keys_value_only,
    clear_export_directory,
)

# from utils import
# from get_random import string
from . import get_random


def test_key_exists():
    """Test the key_exist function"""

    assert get_random.text() is not None

    # Make a random key to find
    search_key = get_random.text()

    # Generate a random dictionary
    search_dict = {}
    for _ in range(get_random.number(0, 5)):
        search_dict[get_random.text()] = get_random.text()

    # No search key, should return False
    assert key_exists(search_key, search_dict) is False

    # Insert the search key
    search_dict[search_key] = get_random.text()

    # Add some more random keys
    for _ in range(get_random.number(0, 5)):
        search_dict[get_random.text()] = get_random.text()

    # Search key, should return True
    assert key_exists(search_key, search_dict) is True


def test_get_debug_all_false():
    """Test that the debug always returns True if any of the args are True"""

    # All false
    assert get_debug(False, {"debug": False}, {"debug": False}) is False


def test_get_debug_variable_true():
    """Test that the debug always returns True if any of the args are True"""

    # Varible True
    assert get_debug(True, {"debug": False}, {"debug": False}) is True
    assert get_debug(True, {"debug": True}, {"debug": False}) is True
    assert get_debug(True, {"debug": False}, {"debug": True}) is True


def test_get_debug_config_true():
    """Test that the debug always returns True if any of the args are True"""

    # Config dict True
    assert get_debug(False, {"debug": True}, {"debug": False}) is True
    assert get_debug(True, {"debug": True}, {"debug": False}) is True
    assert get_debug(False, {"debug": True}, {"debug": True}) is True


def test_get_debug_override_true():
    """Test that the debug always returns True if any of the args are True"""

    # Config override dict True
    assert get_debug(False, {"debug": False}, {"debug": True}) is True
    assert get_debug(True, {"debug": False}, {"debug": True}) is True
    assert get_debug(False, {"debug": True}, {"debug": True}) is True


def test_get_debug_all_true():
    """Test that the debug always returns True if any of the args are True"""

    # All True
    assert get_debug(True, {"debug": True}, {"debug": True}) is True


def test_write_to_file():
    """Test writing to a file"""

    test_filename = "doby_config_test_write_to_file.txt"
    test_directory = get_random.text().upper()
    test_content = get_random.text(100)

    write_to_file(test_filename, test_directory, test_content)

    with open(f"{test_directory}/{test_filename}") as read_file:
        config = read_file.read()

    assert config == test_content + "\n"

    shutil.rmtree(test_directory)


def test_write_list_to_file():
    """Test writing a list to a file"""

    test_filename = "doby_config_test_write_list_to_file.txt"
    test_directory = get_random.text().upper()
    test_content = get_random.text(100)
    test_list = [test_content]

    write_list_to_file(test_filename, test_directory, test_list)

    with open(f"{test_directory}/{test_filename}") as read_file:
        config = read_file.read()

    assert config == f"{test_content}\n"

    shutil.rmtree(test_directory)


def test_indent():
    """Test indent"""

    string_in = get_random.text()

    assert indent(string_in) == string_in
    assert indent(string_in, 1) == "    " + string_in
    assert indent(string_in, 2) == "        " + string_in
    assert indent(string_in, 3) == "            " + string_in
    assert indent(string_in, 4) == "                " + string_in


def test_get_parameters_empty():
    """Test get_parameters_empty"""

    test = {"class": {}}

    assert get_parameters(test, "class") == ""


def test_get_parameters_str_only():
    """Test get_parameters_str"""

    test = {"get_username": {"parameters": {"username": {}}}}

    assert get_parameters(test, "get_username") == ", username"


def test_get_parameters_str():
    """Test get_parameters_str"""

    test = {"class": {"n": "a"}}

    assert get_parameters(test, "class") == ""


def test_get_parameters_type():
    """Test get_parameters_type"""

    test = {
        "class": {
            "parameters": {"debug": {"description": "Enables debugging", "type": "int"}}
        }
    }

    assert get_parameters(test, "class") == ", debug: int"


def test_get_parameters_default_value():
    """Test get_parameters_default_value"""

    test = {
        "class": {
            "parameters": {
                "debug": {
                    "description": "Enables debugging",
                    "defaultValue": True,
                }
            }
        }
    }

    assert get_parameters(test, "class") == ", debug = True"


def test_get_parameters_type_default_value():
    """Test get_parameters_type_default_value"""

    test = {
        "class": {
            "parameters": {
                "debug": {
                    "description": "Enables debugging",
                    "type": "bool",
                    "defaultValue": True,
                }
            }
        }
    }

    assert get_parameters(test, "class") == ", debug: bool = True"


def test_get_parameters_type_default_value_str():
    """Test get_parameters_type_default_value_str"""

    test = {
        "class": {
            "parameters": {
                "debug": {
                    "description": "Enables debugging",
                    "type": "str",
                    "defaultValue": "This is a string",
                }
            }
        }
    }

    assert get_parameters(test, "class") == ', debug: str = "This is a string"'


def test_get_parameters_default_value_str():
    """Test get_parameters_default_value_str"""

    test = {
        "class": {
            "parameters": {
                "debug": {
                    "description": "Enables debugging",
                    "defaultValue": "This is a string",
                }
            }
        }
    }

    assert get_parameters(test, "class") == ', debug = "This is a string"'


def test_get_variable_keys_none():
    """Test get_variable_keys_none"""

    search_dict = {}
    assert (
        generate_dictionary_variable_types("querystring", "pagesize", search_dict)
        is None
    )


def test_get_variable_keys_bad_key():
    """Test get_variable_keys_bad_key"""

    search_dict = {"bad_key": "test()"}
    assert (
        generate_dictionary_variable_types("querystring", "pagesize", search_dict)
        is None
    )


def test_get_variable_keys_function():
    """Test get_variable_keys_function"""

    search_dict = {"function": "test()"}
    assert (
        generate_dictionary_variable_types("querystring", "pagesize", search_dict)
        == 'querystring["pagesize"] = test()'
    )


def test_get_variable_keys_variable():
    """Test get_variable_keys_variable"""

    search_dict = {"variable": "test_var"}
    assert (
        generate_dictionary_variable_types("querystring", "pagesize", search_dict)
        == 'querystring["pagesize"] = test_var'
    )


def test_get_variable_keys_static():
    """Test get_variable_keys_static"""

    search_dict = {"static": 123}
    assert (
        generate_dictionary_variable_types("querystring", "pagesize", search_dict)
        == 'querystring["pagesize"] = 123'
    )

    search_dict = {"static": "123"}
    assert (
        generate_dictionary_variable_types("querystring", "pagesize", search_dict)
        == 'querystring["pagesize"] = "123"'
    )


def test_get_variable_keys_static_special_type():
    """Test get_variable_keys_static_special_type"""

    search_dict = {"static": True}
    assert (
        generate_dictionary_variable_types("querystring", "pagesize", search_dict)
        == 'querystring["pagesize"] = True'
    )

    search_dict = {"static": False}
    assert (
        generate_dictionary_variable_types("querystring", "pagesize", search_dict)
        == 'querystring["pagesize"] = False'
    )

    search_dict = {"static": None}
    assert (
        generate_dictionary_variable_types("querystring", "pagesize", search_dict)
        == 'querystring["pagesize"] = None'
    )

    search_dict = {"static": "True"}
    assert (
        generate_dictionary_variable_types("querystring", "pagesize", search_dict)
        == 'querystring["pagesize"] = True'
    )

    search_dict = {"static": "False"}
    assert (
        generate_dictionary_variable_types("querystring", "pagesize", search_dict)
        == 'querystring["pagesize"] = False'
    )

    search_dict = {"static": "None"}
    assert (
        generate_dictionary_variable_types("querystring", "pagesize", search_dict)
        == 'querystring["pagesize"] = None'
    )


def test_get_variable_keys_value_only_none():
    """Test get_variable_keys_value_only_none"""

    search_dict = {}
    assert get_variable_keys_value_only(search_dict) == ""


def test_get_variable_keys_value_only_bad_key():
    """Test get_variable_keys_value_only_bad_key"""

    search_dict = {"bad_key": "test()"}
    assert get_variable_keys_value_only(search_dict) == ""


def test_get_variable_keys_value_only_function():
    """Test get_variable_keys_value_only_function"""

    search_dict = {"function": "test()"}
    assert get_variable_keys_value_only(search_dict) == "test()"


def test_get_variable_keys_value_only_variable():
    """Test get_variable_keys_value_only_variable"""

    search_dict = {"variable": "test_var"}
    assert get_variable_keys_value_only(search_dict) == "test_var"


def test_get_variable_keys_value_only_static():
    """Test get_variable_keys_value_only_static"""

    search_dict = {"static": 123}
    assert get_variable_keys_value_only(search_dict) == 123

    search_dict = {"static": "123"}
    assert get_variable_keys_value_only(search_dict) == '"123"'


def test_get_variable_keys_value_only_static_special_type():
    """Test get_variable_keys_value_only_static_special_type"""

    search_dict = {"static": True}
    assert get_variable_keys_value_only(search_dict) is True

    search_dict = {"static": False}
    assert get_variable_keys_value_only(search_dict) is False

    search_dict = {"static": None}
    assert get_variable_keys_value_only(search_dict) is None

    search_dict = {"static": "True"}
    assert get_variable_keys_value_only(search_dict) is True

    search_dict = {"static": "False"}
    assert get_variable_keys_value_only(search_dict) is False

    search_dict = {"static": "None"}
    assert get_variable_keys_value_only(search_dict) is None


def test_clear_export_directory():
    """Test deleting the export directory"""

    directory = "pytest_test_dir"

    # Create directory
    if not os.path.isdir(directory):
        os.mkdir("pytest_test_dir")

    # Add files
    write_to_file("/test_output.txt", directory, "hello test")

    # The file exists in the folder
    assert len(glob.glob(directory)) > 0

    # Clear it
    subproc = clear_export_directory(directory)
    assert subproc.returncode == 0
    assert subproc.args == ["rm", "-rf", "pytest_test_dir"]

    assert clear_export_directory("directory_that_doesnt_exist/../") is False
    assert clear_export_directory("directory_that_doesnt_exist") is False

    # The file no longer exists in the folder
    assert len(glob.glob(directory)) == 0

    # Directory should be gone
    assert os.path.isdir(directory) is False
