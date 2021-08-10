"""Doby function testing"""
from doby import Doby
from doby.build import classes
from . import test_config

config_filename = test_config.write_config(test_config.create_test_config())

DOBY = Doby(config_filename=config_filename, debug=True)


def test_get_classes():
    """"Test get_classes"""

    DOBY.reset_config(test_config.create_test_config())
    assert DOBY.get_classes() == [
        "class fruitTest():",
        '    """PyTest configuration library"""',
        "    def __init__(self):",
        '        """Class init"""',
        "",
        "",
        "",
        "        # Requests variables",
        '        self.hostname = self.auth["url"]',
        "        self.debug = debug",
        "",
    ]


def test_get_classes_init_params():
    """Test get_classes_init_params"""

    classes_config = test_config.create_test_config()
    classes_config["functions"]["init"] = {
        "parameters": {
            "debug": {
                "description": "Enables debugging",
                "type": "bool",
                "defaultValue": "False",
            }
        },
        "code": [],
    }
    DOBY.reset_config(classes_config)
    assert DOBY.get_classes() == [
        "class fruitTest():",
        '    """PyTest configuration library"""',
        "    def __init__(self, debug: bool = False):",
        '        """Class init"""',
        "",
        "        # Init code from config",
        "",
        "",
        "        # Requests variables",
        '        self.hostname = self.auth["url"]',
        "        self.debug = debug",
        "",
    ]


def test_get_headers_one():
    """Test get headers with one header"""

    config = {
        "headers": {
            "rest": {
                "Accept": {"static": "application/json"},
                "api-key": {"function": "get_api_key()"},
            }
        }
    }

    assert classes.get_headers(config) == [
        "        # rest headers",
        "        self.rest = {}",
        '        self.rest["Accept"] = "application/json"',
        '        self.rest["api-key"] = get_api_key()',
        "        ",
    ]


def test_get_headers_two():
    """Test get headers with two header"""

    config = {
        "headers": {
            "rest": {
                "Accept": {"static": "application/json"},
                "api-key": {"function": "get_api_key()"},
            }
        },
        "rest_xml": {
            "Accept": {"static": "application/xml"},
            "api-key": {"variable": "api_key"},
        },
    }

    assert classes.get_headers(config) == [
        "        # rest headers",
        "        self.rest = {}",
        '        self.rest["Accept"] = "application/json"',
        '        self.rest["api-key"] = get_api_key()',
        "        ",
    ]


def test_get_http_response_function_one():
    """Test get http response with one header"""

    config = {
        "debug": True,
        "hostname": {"variable": "get_url()"},
        "headers": {
            "rest": {
                "Accept": {"static": "application/json"},
                "api-key": {"function": "get_api_key()"},
            }
        },
    }

    assert classes.get_http_response_function(config) == [
        "        # Requests variables",
        "        self.hostname = get_url()",
        "        self.debug = debug",
    ]


def test_get_http_response_function_two():
    """Test get http response with two header"""

    config = {
        "debug": True,
        "hostname": {"static": "example.com"},
        "headers": {
            "rest": {
                "Accept": {"static": "application/json"},
                "api-key": {"function": "get_api_key()"},
            },
            "rest_xml": {
                "Accept": {"static": "application/xml"},
                "api-key": {"variable": "api_key"},
            },
        },
    }

    assert classes.get_http_response_function(config) == [
        "        # Requests variables",
        '        self.hostname = "example.com"',
        "        self.debug = debug",
    ]
