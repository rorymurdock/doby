"""Doby generator parameters testing"""
from doby.generator import parameters


def test_querystring():
    """Test querystring"""

    assert parameters.querystring({}) == {}


def test_get_querystring_empty():
    """Test get_querystring_empty"""

    assert parameters.querystring({}) == {}


def test_get_querystring():
    """Test get_querystring"""

    assert parameters.querystring([{"name": "test", "in": "path"}]) == {}


def test_get_querystring_in_qs():
    """Test get_querystring_in_qs"""

    assert parameters.querystring([{"name": "test", "in": "query"}]) == {
        "test": {"variable": "test"}
    }


def test_get_parameters_empty():
    """Test get_parameters_empty"""

    assert parameters.get_parameters({}) == {}


def test_get_parameters_no_description():
    """Test get_parameters_no_description"""

    assert parameters.get_parameters([{"name": "test"}]) == {}


def test_get_parameters_description():
    """Test get_parameters_description"""

    assert parameters.get_parameters([{"name": "test", "description": "pytest"}]) == {
        "test": {"description": "pytest"}
    }


def test_get_parameters_description_required():
    """Test get_parameters_description_required"""

    assert parameters.get_parameters(
        [{"name": "test", "description": "pytest", "required": True}]
    ) == {"test": {"description": "pytest"}}


def test_get_parameters_description_required_false():
    """Test get_parameters_description_required_false"""

    assert parameters.get_parameters(
        [{"name": "test", "description": "pytest", "required": False}]
    ) == {"test": {"defaultValue": "None", "description": "pytest"}}


def test_get_parameters_description_type():
    """Test get_parameters_description_type"""

    assert parameters.get_parameters(
        [{"name": "test", "description": "pytest", "type": "int32"}]
    ) == {"test": {"description": "pytest", "type": "int"}}


def test_get_parameters_description_required_type():
    """Test get_parameters_description_required_type"""

    assert parameters.get_parameters(
        [{"name": "test", "description": "pytest", "required": True, "type": "int32"}]
    ) == {"test": {"description": "pytest", "type": "int"}}


# def test_find_parameter_refs():
#     parameters.find_parameter_refs()
