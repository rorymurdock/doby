"""Doby README testing"""
from doby.build.readme import format_function, build_readme
from . import test_config


def test_format_function_name_no_key():
    """Test format_function_name_no_key"""

    function = {}
    function["fruitTest"] = {}

    assert format_function("fruitTest", function) == ["### fruitTest()", ""]


def test_format_function_name():
    """Test format_function_name"""

    function = {}
    function["fruitTest"] = {}
    function["fruitTest"]["name"] = "fruitTest"

    assert format_function("fruitTest", function) == ["### fruitTest()", ""]


def test_format_function_description():
    """Test format_function_description"""

    function = {}
    function["fruitTest"] = {}
    function["fruitTest"]["name"] = "fruitTest"
    function["fruitTest"]["description"] = "This is the description of fruitTest"

    assert format_function("fruitTest", function) == [
        "### fruitTest()",
        "",
        "This is the description of fruitTest",
        "",
    ]


def test_format_function_parameters_empty():
    """Test format_function_parameters_empty"""

    function = {}
    function["fruitTest"] = {}
    function["fruitTest"]["name"] = "fruitTest"
    function["fruitTest"]["parameters"] = {}

    assert format_function("fruitTest", function) == [
        "### fruitTest()",
        "",
    ]


def test_format_function_parameters_desc_type_default():
    """Test format_function_parameters_desc_type_default"""

    function = {}
    function["fruitTest"] = {}
    function["fruitTest"]["name"] = "fruitTest"
    function["fruitTest"]["parameters"] = {}
    function["fruitTest"]["parameters"]["debug"] = {}
    function["fruitTest"]["parameters"]["debug"]["description"] = "Enables debugging"
    function["fruitTest"]["parameters"]["debug"]["type"] = "bool"
    function["fruitTest"]["parameters"]["debug"]["defaultValue"] = True

    assert format_function("fruitTest", function) == [
        "### fruitTest()",
        "",
        "|Name|Description|Type|Default value|",
        "|-|-|-|-|",
        "|debug|Enables debugging|bool|True|",
        "",
    ]


def test_format_function_parameters_desc_type():
    """Test format_function_parameters_desc_type"""

    function = {}
    function["fruitTest"] = {}
    function["fruitTest"]["name"] = "fruitTest"
    function["fruitTest"]["parameters"] = {}
    function["fruitTest"]["parameters"]["debug"] = {}
    function["fruitTest"]["parameters"]["debug"]["description"] = "Enables debugging"
    function["fruitTest"]["parameters"]["debug"]["type"] = "bool"

    assert format_function("fruitTest", function) == [
        "### fruitTest()",
        "",
        "|Name|Description|Type|Default value|",
        "|-|-|-|-|",
        "|debug|Enables debugging|bool||",
        "",
    ]


def test_format_function_parameters_desc():
    """Test format_function_parameters_desc"""

    function = {}
    function["fruitTest"] = {}
    function["fruitTest"]["name"] = "fruitTest"
    function["fruitTest"]["parameters"] = {}
    function["fruitTest"]["parameters"]["debug"] = {}
    function["fruitTest"]["parameters"]["debug"]["description"] = "Enables debugging"

    assert format_function("fruitTest", function) == [
        "### fruitTest()",
        "",
        "|Name|Description|Type|Default value|",
        "|-|-|-|-|",
        "|debug|Enables debugging|||",
        "",
    ]


def test_format_function_parameters_type():
    """Test format_function_parameters_type"""

    function = {}
    function["fruitTest"] = {}
    function["fruitTest"]["name"] = "fruitTest"
    function["fruitTest"]["parameters"] = {}
    function["fruitTest"]["parameters"]["debug"] = {}
    function["fruitTest"]["parameters"]["debug"]["type"] = "bool"

    assert format_function("fruitTest", function) == [
        "### fruitTest()",
        "",
        "|Name|Description|Type|Default value|",
        "|-|-|-|-|",
        "|debug||bool||",
        "",
    ]


def test_format_function_returns():
    """Test format_function_returns"""

    function = {}
    function["fruitTest"] = {}
    function["fruitTest"]["name"] = "fruitTest"
    function["fruitTest"]["returns"] = "response.txt"

    assert format_function("fruitTest", function) == [
        "### fruitTest()",
        "",
        "Returns: `response.txt`",
        "",
    ]


def test_format_function_check_http_response():
    """Test format_function_checkHttpResponse"""

    function = {}
    function["fruitTest"] = {}
    function["fruitTest"]["name"] = "fruitTest"
    function["fruitTest"]["checkHttpResponse"] = True

    assert format_function("fruitTest", function) == [
        "### fruitTest()",
        "",
        "The response will be checked",
        "",
    ]


def test_format_function_main_run():
    """Test format_function_main_run"""

    function = {}
    function["fruitTest"] = {}
    function["fruitTest"]["name"] = "fruitTest"
    function["fruitTest"]["run"] = True

    assert format_function("fruitTest", function) == [
        "### fruitTest()",
        "",
        "This function will run if launched directly",
        "",
    ]


def test_build_readme():
    """Test build_readme"""

    config = test_config.create_test_config()

    assert build_readme(config) == [
        "# fruitTest",
        "",
        "PyTest configuration library",
        "",
        "## Default functions",
        "",
    ]


def test_build_readme_init():
    """Test build_readme_init"""

    config = test_config.create_test_config()
    config["functions"]["init"] = {}
    config["functions"]["init"][
        "description"
    ] = "This is called when the class is initialised"
    config["functions"]["init"]["parameters"] = {}
    config["functions"]["init"]["parameters"]["debug"] = {}
    config["functions"]["init"]["parameters"]["debug"][
        "description"
    ] = "Enables debugging"
    config["functions"]["init"]["parameters"]["debug"]["type"] = "bool"
    config["functions"]["init"]["parameters"]["debug"]["defaultValue"] = "False"

    assert build_readme(config) == [
        "# fruitTest",
        "",
        "PyTest configuration library",
        "",
        "## Default functions",
        "",
        "### init()",
        "",
        "This is called when the class is initialised",
        "",
        "|Name|Description|Type|Default value|",
        "|-|-|-|-|",
        "|debug|Enables debugging|bool|False|",
        "",
    ]


def test_build_readme_init_main():
    """Test build_readme_init_main"""

    config = test_config.create_test_config()
    config["functions"]["init"] = {}
    config["functions"]["init"][
        "description"
    ] = "This is called when the class is initialised"
    config["functions"]["init"]["parameters"] = {}
    config["functions"]["init"]["parameters"]["debug"] = {}
    config["functions"]["init"]["parameters"]["debug"][
        "description"
    ] = "Enables debugging"
    config["functions"]["init"]["parameters"]["debug"]["type"] = "bool"
    config["functions"]["init"]["parameters"]["debug"]["defaultValue"] = "False"

    config["functions"]["main"] = {}
    config["functions"]["main"]["run"] = True
    config["functions"]["main"]["description"] = "This is the main function"
    config["functions"]["main"]["code"] = [
        "uem = WSO()",
        'print(uem.systemInfo()["ProductVersion"])',
    ]

    assert build_readme(config) == [
        "# fruitTest",
        "",
        "PyTest configuration library",
        "",
        "## Default functions",
        "",
        "### init()",
        "",
        "This is called when the class is initialised",
        "",
        "|Name|Description|Type|Default value|",
        "|-|-|-|-|",
        "|debug|Enables debugging|bool|False|",
        "",
        "### main()",
        "",
        "This is the main function",
        "",
        "This function will run if launched directly",
        "",
    ]


def test_build_readme_init_main_endpoint():
    """Test build_readme_init_main_endpoint"""

    config = test_config.create_test_config()
    config["functions"]["init"] = {}
    config["functions"]["init"][
        "description"
    ] = "This is called when the class is initialised"
    config["functions"]["init"]["parameters"] = {}
    config["functions"]["init"]["parameters"]["debug"] = {}
    config["functions"]["init"]["parameters"]["debug"][
        "description"
    ] = "Enables debugging"
    config["functions"]["init"]["parameters"]["debug"]["type"] = "bool"
    config["functions"]["init"]["parameters"]["debug"]["defaultValue"] = "False"

    config["functions"]["main"] = {}
    config["functions"]["main"]["run"] = True
    config["functions"]["main"]["description"] = "This is the main function"
    config["functions"]["main"]["code"] = [
        "uem = WSO()",
        'print(uem.systemInfo()["ProductVersion"])',
    ]
    config["functions"]["endpoint"] = {
        "systemInfo": {
            "category": "SystemAPIs",
            "name": "systemInfo",
            "description": "Gets System information",
            "method": "get",
            "path": "/api/system/info",
            "response": "response.txt",
            "header": "api-v1",
            "returns": "response.text",
            "checkHttpResponse": True,
            "payload": {
                "static": "cn135.awmdm.com",
                "variable": "url",
                "function": "get_url()",
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
        }
    }

    assert build_readme(config) == [
        "# fruitTest",
        "",
        "PyTest configuration library",
        "",
        "## Default functions",
        "",
        "### init()",
        "",
        "This is called when the class is initialised",
        "",
        "|Name|Description|Type|Default value|",
        "|-|-|-|-|",
        "|debug|Enables debugging|bool|False|",
        "",
        "### main()",
        "",
        "This is the main function",
        "",
        "This function will run if launched directly",
        "",
        "## Endpoint functions",
        "",
        "### systemInfo()",
        "",
        "Gets System information",
        "",
        "|Name|Description|Type|Default value|",
        "|-|-|-|-|",
        "|pagesize|How many results to return|int|500|",
        "|page|Which page of results to return|int|0|",
        "",
        "Returns: `response.text`",
        "",
        "The response will be checked",
        "",
    ]
