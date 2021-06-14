"""Doby generator normalise testing"""
from doby.generator import normalise
from . import get_random


def test_safe_variable():
    """Test safe_variable"""
    test_str = get_random.text()
    assert normalise.safe_variable(test_str) == test_str
    assert (
        normalise.safe_variable(test_str[:4] + "/" + test_str[4:])
        == test_str[:4] + "/" + test_str[4:]
    )
    assert normalise.safe_variable("test{ing") == "testing"
    assert normalise.safe_variable("test}ing") == "testing"
    assert normalise.safe_variable("test-ing") == "testing"
    assert normalise.safe_variable("test:ing") == "testing"
    assert normalise.safe_variable("test.ing") == "testing"


def test_path():
    """Test path"""
    test_str = get_random.text()
    assert normalise.path("test") == "Test"
    assert normalise.path("test", True) == "test"

    for cull_char in ["/", "{", "}", "-", ":", "."]:
        assert (
            normalise.path(test_str[:4] + cull_char + test_str[4:])
            == test_str.capitalize()
        )

    assert (
        normalise.path(test_str[:4] + "%" + test_str[4:])
        == (test_str[:4] + "%" + test_str[4:]).capitalize()
    )


def test_dynamic_path():
    """Test dynamicPath"""
    test_str = get_random.text()
    assert (
        normalise.dynamic_path(test_str[:4] + "-" + test_str[4:])
        == test_str[:4] + "-" + test_str[4:]
    )

    for cull_char in ["/", "{", "}", ":", "."]:
        assert (
            normalise.dynamic_path(test_str[:4] + cull_char + test_str[4:])
            == test_str[:4] + cull_char + test_str[4:]
        )


def test_version():
    """Test version"""
    assert normalise.version([]) == 1
    assert normalise.version(["application/json"]) == 1
    assert normalise.version(["application/json;version=2"]) == 2
    assert normalise.version(["application/json;version=3"]) == 3
    assert normalise.version(["application/json;version=4"]) == 4


def test_normalise_type():
    """Test normalise_type"""

    assert normalise.normalise_type("") == "str"
    assert normalise.normalise_type("bad_type") == "str"
    assert normalise.normalise_type("uuid") == "str"
    assert normalise.normalise_type("String") == "str"
    assert normalise.normalise_type("string") == "str"
    assert normalise.normalise_type("None") == "str"
    assert normalise.normalise_type("int32") == "int"
    assert normalise.normalise_type("integer") == "int"
    assert normalise.normalise_type("boolean") == "bool"


# def path(input_str, skip_caps=False):
#     """Remove certain special characters from string"""
#     elemnts = ["/", "{", "}", "-", ":", "."]
#     for elemnt in elemnts:
#         input_str = input_str.replace(elemnt, "")

#     if not skip_caps:
#         input_str = input_str.capitalize()

#     # logging.info("Normalised string")
#     return input_str
