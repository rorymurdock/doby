"""Doby function testing"""
from doby.build import functions


def test_function_code_exists_no_dict():
    """Test function_code_exists_no_dict"""

    function = {}
    assert functions.function_code_exists("start", function) is False


def test_function_code_exists_empty_dict():
    """Test function_code_exists_empty_dict"""

    function = {"code": {}}
    assert functions.function_code_exists("start", function) is False


def test_function_code_exists_start():
    """Test function_code_exists_start"""

    function = {"name": "code_test", "code": {"start": ["line 1"]}}
    assert functions.function_code_exists("start", function) is True


def test_function_code_exists_mid():
    """Test function_code_exists_mid"""

    function = {"name": "code_test", "code": {"mid": ["line 2"]}}
    assert functions.function_code_exists("mid", function) is True


def test_function_code_exists_end():
    """Test function_code_exists_end"""

    function = {"name": "code_test", "code": {"end": ["line 3"]}}
    assert functions.function_code_exists("end", function) is True


def test_function_code_exists_all():
    """Test function_code_exists_all"""

    function = {
        "name": "code_test",
        "code": {"start": ["line 1"], "mid": ["line 2"], "end": ["line 3"]},
    }
    assert functions.function_code_exists("start", function) is True
    assert functions.function_code_exists("mid", function) is True
    assert functions.function_code_exists("end", function) is True


def test_function_code_exists_custom_code():
    """Test function_code_exists_all_custom_code"""

    function = {"name": "code_test", "code": ["line 1"]}
    assert functions.function_code_exists("start", function) is False


def test_get_function_code_no_dict():
    """Test get_function_code_no_dict"""

    function = {}
    assert functions.get_function_code("start", function) == []


def test_get_function_code_empty_dict():
    """Test get_function_code_empty_dict"""

    function = {"code": {}}
    assert functions.get_function_code("start", function) == []


def test_get_function_code_start():
    """Test get_function_code_start"""

    function = {"name": "code_test", "code": {"start": ["line 1"]}}
    assert functions.get_function_code("start", function) == ["        line 1"]


def test_get_function_code_mid():
    """Test get_function_code_mid"""

    function = {"name": "code_test", "code": {"mid": ["line 2"]}}
    assert functions.get_function_code("mid", function) == ["        line 2"]


def test_get_function_code_end():
    """Test get_function_code_end"""

    function = {"name": "code_test", "code": {"end": ["line 3"]}}
    assert functions.get_function_code("end", function) == ["        line 3"]


def test_get_function_code_all():
    """Test get_function_code_all"""

    function = {
        "name": "code_test",
        "code": {"start": ["line 1"], "mid": ["line 2"], "end": ["line 3"]},
    }
    assert functions.get_function_code("start", function) == ["        line 1"]
    assert functions.get_function_code("mid", function) == ["        line 2"]
    assert functions.get_function_code("end", function) == ["        line 3"]


def test_querystring_exists_no_dict():
    """Test querystring_exists_no_dict"""

    function = {}
    assert functions.querystring_exists(function) is False


def test_querystring_exists_empty_dict():
    """Test querystring_exists_empty_dict"""

    function = {"querystring": {}}
    assert functions.querystring_exists(function) is True


def test_get_querystring_no_dict():
    """Test get_querystring_no_dict"""

    function = {"name": "code_test"}
    assert functions.get_querystring(function) == []


def test_querystring_exists_name_empty_dict():
    """Test querystring_exists_name_empty_dict"""

    function = {"name": "code_test", "querystring": {}}
    assert functions.get_querystring(function) == ["        querystring = {}", ""]


def test_get_querystring():
    """Test get_querystring"""

    function = {
        "name": "code_test",
        "querystring": {
            "bool_test": {"static": True},
            "pagesize": {"static": 500},
            "page": {"variable": "page"},
            "apikey": {"function": "get_api_key()"},
        },
    }
    assert functions.get_querystring(function) == [
        "        querystring = {}",
        '        querystring["bool_test"] = True',
        '        querystring["pagesize"] = 500',
        '        querystring["page"] = page',
        '        querystring["apikey"] = get_api_key()',
        "",
    ]


def test_payload_exists_no_dict():
    """Test payload_exists_no_dict"""

    function = {}
    assert functions.payload_exists(function) is False


def test_payload_exists_empty_dict():
    """Test payload_exists_empty_dict"""

    function = {"payload": {}}
    assert functions.payload_exists(function) is True


def test_get_payload_no_dict():
    """Test get_payload_no_dict"""

    function = {"name": "code_test"}
    assert functions.get_payload(function) == []


def test_payload_exists_name_empty_dict():
    """Test payload_exists_name_empty_dict"""

    function = {"name": "code_test", "payload": {}}
    assert functions.get_payload(function) == ["        payload = {}", ""]


def test_get_payload():
    """Test get_payload"""

    function = {
        "name": "code_test",
        "payload": {
            "bool_test": {"static": True},
            "pagesize": {"static": 500},
            "page": {"variable": "page"},
            "apikey": {"function": "get_api_key()"},
        },
    }
    assert functions.get_payload(function) == [
        "        payload = {}",
        '        payload["bool_test"] = True',
        '        payload["pagesize"] = 500',
        '        payload["page"] = page',
        '        payload["apikey"] = get_api_key()',
        "",
    ]


def test_get_http_response_querystring_payload():
    """Test get_http_response_querystring_payload"""

    function = {
        "name": "code_test",
        "header": "api",
        "method": "get",
        "path": "/test/api",
        "querystring": {},
        "payload": {},
    }
    assert functions.get_http_response(function) == [
        '        response = self.api.get(f"/test/api", querystring=querystring, '
        "payload=payload)",
        "",
    ]


def test_get_http_response_querystring():
    """Test get_http_response_querystring"""

    function = {
        "name": "code_test",
        "header": "api",
        "method": "get",
        "path": "/test/api",
        "querystring": {},
    }
    assert functions.get_http_response(function) == [
        '        response = self.api.get(f"/test/api", querystring=querystring)',
        "",
    ]


def test_get_http_response():
    """Test get_http_response"""

    function = {
        "name": "code_test",
        "header": "api",
        "method": "get",
        "path": "/test/api",
    }
    assert functions.get_http_response(function) == [
        '        response = self.api.get(f"/test/api")',
        "",
    ]


def test_check_http_response_exists_true():
    """Test check_http_response_exists_true"""

    function = {"checkHttpResponse": True}
    assert functions.check_http_response_exists(function) is True


def test_check_http_response_exists_false():
    """Test check_http_response_exists_false"""

    function = {}
    assert functions.check_http_response_exists(function) is False


def test_get_check_http_response():
    """Test get_check_http_response"""

    function = {"name": "code_test", "checkHttpResponse": True}
    assert functions.get_check_http_response(function) == [
        "        if self.check_http_response(response):",
        "            return json.loads(response.text)",
        "        else:",
        "            logging.error('Error with HTTP request')",
        "            return False",
        "",
    ]


def test_get_check_http_response_no_key():
    """Test get_check_http_response"""

    function = {}
    assert functions.get_check_http_response(function) == []


def test_get_check_http_response_expected_code():
    """Test get_check_http_response"""

    function = {"name": "code_test", "checkHttpResponse": True, "expectedHttpCode": 202}
    assert functions.get_check_http_response(function) == [
        "        if self.check_http_response(response, 202):",
        "            return json.loads(response.text)",
        "        else:",
        "            logging.error('Error with HTTP request')",
        "            return False",
        "",
    ]


def test_return_exists_true():
    """Test return_exists_true"""

    function = {"return": "response.txt"}
    assert functions.return_exists(function) is True


def test_return_exists_false():
    """Test return_exists_false"""

    function = {}
    assert functions.return_exists(function) is False


def test_get_return_no_dict():
    """Test get_return_no_dict"""

    function = {}
    assert functions.return_exists(function) is False


def test_get_return():
    """Test get_return"""

    function = {"return": "response.txt"}
    assert functions.get_return(function) == ["        return response.txt"]


def test_get_return_no_key():
    """Test get_return"""

    function = {}
    assert functions.get_return(function) == []


def test_build_functions_empty():
    """Test build_functions_empty"""

    config = {}
    config["functions"] = {}
    assert functions.build_functions(config) == []


def test_build_functions_missing_keys():
    """Test build_functions_missing_keys"""

    config = {}
    config["functions"] = {}
    config["functions"]["endpoint"] = {}
    config["functions"]["endpoint"]["peel_fruit"] = {}
    fruit = config["functions"]["endpoint"]["peel_fruit"]
    fruit["description"] = "Let's peel"
    fruit["header"] = "api"
    fruit["method"] = "get"
    fruit["path"] = "/api/system/info"

    assert functions.build_functions(config) == []


def test_build_functions_basic():
    """Test build_functions_basic"""

    config = {}
    config["functions"] = {}
    config["functions"]["endpoint"] = {}
    config["functions"]["endpoint"]["peel_fruit"] = {}
    fruit = config["functions"]["endpoint"]["peel_fruit"]
    fruit["name"] = "code_test"
    fruit["description"] = "Let's peel"
    fruit["header"] = "api"
    fruit["method"] = "get"
    fruit["path"] = "/api/system/info"
    fruit["return"] = "response.text"

    assert functions.build_functions(config) == [
        "    def code_test(self):",
        '        """Let\'s peel"""',
        '        response = self.api.get(f"/api/system/info")',
        "",
        "        return response.text",
    ]


def test_build_functions_code_start():
    """Test build_functions_code_start"""

    config = {}
    config["functions"] = {}
    config["functions"]["endpoint"] = {}
    config["functions"]["endpoint"]["peel_fruit"] = {}
    fruit = config["functions"]["endpoint"]["peel_fruit"]
    fruit["name"] = "code_test"
    fruit["description"] = "Let's peel"
    fruit["header"] = "api"
    fruit["method"] = "get"
    fruit["path"] = "/api/system/info"
    fruit["return"] = "response.text"
    fruit["code"] = {}
    fruit["code"]["start"] = ["line 1"]

    assert functions.build_functions(config) == [
        "    def code_test(self):",
        '        """Let\'s peel"""',
        "        line 1",
        '        response = self.api.get(f"/api/system/info")',
        "",
        "        return response.text",
    ]


def test_build_functions_querystring():
    """Test build_functions_querystring"""

    config = {}
    config["functions"] = {}
    config["functions"]["endpoint"] = {}
    config["functions"]["endpoint"]["peel_fruit"] = {}
    fruit = config["functions"]["endpoint"]["peel_fruit"]
    fruit["name"] = "code_test"
    fruit["description"] = "Let's peel"
    fruit["header"] = "api"
    fruit["method"] = "get"
    fruit["path"] = "/api/system/info"
    fruit["return"] = "response.text"
    fruit["querystring"] = {
        "pagesize": {"static": 500},
        "page": {"variable": "page"},
        "apikey": {"function": "get_api_key()"},
    }

    assert functions.build_functions(config) == [
        "    def code_test(self):",
        '        """Let\'s peel"""',
        "        querystring = {}",
        '        querystring["pagesize"] = 500',
        '        querystring["page"] = page',
        '        querystring["apikey"] = get_api_key()',
        "",
        '        response = self.api.get(f"/api/system/info", querystring=querystring)',
        "",
        "        return response.text",
    ]


def test_build_functions_payload():
    """Test build_functions_payload"""

    config = {}
    config["functions"] = {}
    config["functions"]["endpoint"] = {}
    config["functions"]["endpoint"]["peel_fruit"] = {}
    fruit = config["functions"]["endpoint"]["peel_fruit"]
    fruit["name"] = "code_test"
    fruit["description"] = "Let's peel"
    fruit["header"] = "api"
    fruit["method"] = "get"
    fruit["path"] = "/api/system/info"
    fruit["return"] = "response.text"
    fruit["payload"] = {
        "pagesize": {"static": 500},
        "page": {"variable": "page"},
        "apikey": {"function": "get_api_key()"},
    }

    assert functions.build_functions(config) == [
        "    def code_test(self):",
        '        """Let\'s peel"""',
        "        payload = {}",
        '        payload["pagesize"] = 500',
        '        payload["page"] = page',
        '        payload["apikey"] = get_api_key()',
        "",
        '        response = self.api.get(f"/api/system/info", payload=payload)',
        "",
        "        return response.text",
    ]


def test_build_functions_code_mid():
    """Test build_functions_code_mid"""

    config = {}
    config["functions"] = {}
    config["functions"]["endpoint"] = {}
    config["functions"]["endpoint"]["peel_fruit"] = {}
    fruit = config["functions"]["endpoint"]["peel_fruit"]
    fruit["name"] = "code_test"
    fruit["description"] = "Let's peel"
    fruit["header"] = "api"
    fruit["method"] = "get"
    fruit["path"] = "/api/system/info"
    fruit["return"] = "response.text"
    fruit["code"] = {}
    fruit["code"]["mid"] = ["line 2"]

    assert functions.build_functions(config) == [
        "    def code_test(self):",
        '        """Let\'s peel"""',
        "        line 2",
        '        response = self.api.get(f"/api/system/info")',
        "",
        "        return response.text",
    ]


def test_check_http_response_exists():
    """Test check_http_response_exists"""

    config = {}
    config["functions"] = {}
    config["functions"]["endpoint"] = {}
    config["functions"]["endpoint"]["peel_fruit"] = {}
    fruit = config["functions"]["endpoint"]["peel_fruit"]
    fruit["name"] = "code_test"
    fruit["description"] = "Let's peel"
    fruit["header"] = "api"
    fruit["method"] = "get"
    fruit["path"] = "/api/system/info"
    fruit["return"] = "response.text"

    assert functions.build_functions(config) == [
        "    def code_test(self):",
        '        """Let\'s peel"""',
        '        response = self.api.get(f"/api/system/info")',
        "",
        "        return response.text",
    ]


def test_build_functions_code_end():
    """Test build_functions_code_end"""

    config = {}
    config["functions"] = {}
    config["functions"]["endpoint"] = {}
    config["functions"]["endpoint"]["peel_fruit"] = {}
    fruit = config["functions"]["endpoint"]["peel_fruit"]
    fruit["name"] = "code_test"
    fruit["description"] = "Let's peel"
    fruit["header"] = "api"
    fruit["method"] = "get"
    fruit["path"] = "/api/system/info"
    fruit["checkHttpResponse"] = True
    fruit["code"] = {}
    fruit["code"]["end"] = ["line 3"]

    assert functions.build_functions(config) == [
        "    def code_test(self):",
        '        """Let\'s peel"""',
        '        response = self.api.get(f"/api/system/info")',
        "",
        "        if self.check_http_response(response):",
        "            return json.loads(response.text)",
        "        else:",
        "            logging.error('Error with HTTP request')",
        "            return False",
        "",
        "        line 3",
        "    def check_http_response(self, response, expected_code=None):",
        '        """Checks if response is a expected or a known good response"""',
        "    ",
        "        status_codes = {}",
        "        status_codes[200] = True, 'HTTP 200: OK'",
        "        status_codes[201] = True, 'HTTP 201: Created'",
        "        status_codes[202] = True, 'HTTP 202: Accepted'",
        "        status_codes[204] = True, 'HTTP 204: Empty Response'",
        "        status_codes[400] = False, 'HTTP 400: Bad Request'",
        "        status_codes[401] = False, 'HTTP 401: Check WSO Credentials'",
        "        status_codes[403] = False, 'HTTP 403: Permission denied'",
        "        status_codes[404] = False, 'HTTP 404: Not found'",
        "        status_codes[406] = False, 'HTTP 406: Not Acceptable'",
        "        status_codes[422] = False, 'HTTP 422: Invalid searchby Parameter'",
        "        status_codes[500] = False, 'HTTP 500: Internal server error'",
        "",
        '        # Check if a HTTP code is a "good" code',
        "        if response.status_code == expected_code:",
        "            return True",
        "    ",
        "        # Lookup the code in the dict",
        "        elif response.status_code in status_codes:",
        "            logging.debug(status_codes[response.status_code][1])",
        "            if response.status_code != 200:",
        "                # Show the body for non 200",
        "                logging.debug(response.text)",
        "            return status_codes[response.status_code][0]",
        "",
        "        # Unable to find code return False",
        "        else:",
        "            logging.error('Unknown code %s', response.status_code)",
        "            return False",
        "",
    ]


def test_build_functions_all():
    """Test build_functions_all"""

    config = {}
    config["functions"] = {}
    config["functions"]["endpoint"] = {}
    config["functions"]["endpoint"]["peel_fruit"] = {}
    fruit = config["functions"]["endpoint"]["peel_fruit"]
    fruit["name"] = "code_test"
    fruit["description"] = "Let's peel"
    fruit["header"] = "api"
    fruit["method"] = "get"
    fruit["path"] = "/api/system/info"
    fruit["return"] = "response.text"
    fruit["code"] = {}
    fruit["code"]["start"] = ["line 1"]
    fruit["code"]["mid"] = ["line 2"]
    fruit["code"]["end"] = ["line 3"]
    fruit["querystring"] = {
        "pagesize": {"static": 500},
        "page": {"variable": "page"},
        "apikey": {"function": "get_api_key()"},
    }
    fruit["payload"] = {
        "pagesize": {"static": 500},
        "page": {"variable": "page"},
        "apikey": {"function": "get_api_key()"},
    }
    fruit["checkHttpResponse"] = True
    fruit = config["functions"]["custom"] = {}
    fruit = config["functions"]["custom"]["apples"] = {
        "name": "get_api_key",
        "description": "Custom test description",
        "code": ['return self.auth["api-key"]'],
    }

    assert functions.build_functions(config) == [
        "    def code_test(self):",
        '        """Let\'s peel"""',
        "        line 1",
        "        querystring = {}",
        '        querystring["pagesize"] = 500',
        '        querystring["page"] = page',
        '        querystring["apikey"] = get_api_key()',
        "",
        "        payload = {}",
        '        payload["pagesize"] = 500',
        '        payload["page"] = page',
        '        payload["apikey"] = get_api_key()',
        "",
        "        line 2",
        '        response = self.api.get(f"/api/system/info", querystring=querystring, '
        "payload=payload)",
        "",
        "        if self.check_http_response(response):",
        "            return json.loads(response.text)",
        "        else:",
        "            logging.error('Error with HTTP request')",
        "            return False",
        "",
        "        line 3",
        "        return response.text",
        "    def get_api_key(self):",
        '        """Custom test description"""',
        '        return self.auth["api-key"]',
        "",
        "    def check_http_response(self, response, expected_code=None):",
        '        """Checks if response is a expected or a known good response"""',
        "    ",
        "        status_codes = {}",
        "        status_codes[200] = True, 'HTTP 200: OK'",
        "        status_codes[201] = True, 'HTTP 201: Created'",
        "        status_codes[202] = True, 'HTTP 202: Accepted'",
        "        status_codes[204] = True, 'HTTP 204: Empty Response'",
        "        status_codes[400] = False, 'HTTP 400: Bad Request'",
        "        status_codes[401] = False, 'HTTP 401: Check WSO Credentials'",
        "        status_codes[403] = False, 'HTTP 403: Permission denied'",
        "        status_codes[404] = False, 'HTTP 404: Not found'",
        "        status_codes[406] = False, 'HTTP 406: Not Acceptable'",
        "        status_codes[422] = False, 'HTTP 422: Invalid searchby Parameter'",
        "        status_codes[500] = False, 'HTTP 500: Internal server error'",
        "",
        '        # Check if a HTTP code is a "good" code',
        "        if response.status_code == expected_code:",
        "            return True",
        "    ",
        "        # Lookup the code in the dict",
        "        elif response.status_code in status_codes:",
        "            logging.debug(status_codes[response.status_code][1])",
        "            if response.status_code != 200:",
        "                # Show the body for non 200",
        "                logging.debug(response.text)",
        "            return status_codes[response.status_code][0]",
        "",
        "        # Unable to find code return False",
        "        else:",
        "            logging.error('Unknown code %s', response.status_code)",
        "            return False",
        "",
    ]
