"""Doby functions build testing"""
import logging
from doby import utils


def build_functions(config):
    """Build functions from config"""

    functions_out = []

    # Used to add checkHttpResponse function if required
    add_check_http_response = False
    add_filter_querystring = False

    for function_category_name in ["endpoint", "custom"]:
        if utils.key_exists(function_category_name, config["functions"]):
            logging.info("Searching function category %s",
                         function_category_name)
            for function_name in config["functions"][function_category_name]:
                logging.info("Building function %s", function_name)

                # Alias the function
                function = config["functions"][function_category_name][
                    function_name]
                function_cat = config["functions"][function_category_name]
                function_out = []

                # Check that all required keys are present
                if function_category_name == "endpoint":
                    skip = False
                    for key in [
                            "name", "description", "header", "method", "path"
                    ]:
                        if not utils.key_exists(key, function):
                            logging.error(
                                "No %s found for function %s:%s, skipping function",
                                key, function_category_name, function_name)
                            skip = True
                    if skip:
                        # Something's missing, skip this one
                        continue

                # Function def and description
                function_name_key = config["functions"][
                    function_category_name][function_name]["name"]
                function_out.append(
                    utils.indent(
                        f"def {function_name_key}(self{utils.get_parameters(function_cat, function_name)}):",
                        1))
                if "\n" in function['description']:
                    # Multiline description
                    function_out.append(utils.indent("\"\"\"", 2))
                    # 0 indent for better black formatting
                    function_out.append(
                        utils.indent(f"{function['description']}", 0))
                    function_out.append(utils.indent("\"\"\"", 2))
                else:
                    # Single line description
                    function_out.append(
                        utils.indent(f"\"\"\"{function['description']}\"\"\"",
                                     2))

                function_out.append("")  # Add a new line

                if utils.key_exists("code", function):
                    if isinstance(function["code"], list):
                        for line in function["code"]:
                            function_out.append(utils.indent(line, 2))
                        function_out.append("")

                # Insert start code
                if function_code_exists("start", function):
                    logging.info("%s:%s adding start code",
                                 function_category_name, function_name)
                    function_out += get_function_code("start", function)

                # Get querystring
                if querystring_exists(function):
                    logging.info("%s:%s adding querystring",
                                 function_category_name, function_name)
                    function_out += get_querystring(function)

                # Insert the code to filter the querystring
                if querystring_filter_exists(function) and querystring_exists(
                        function):
                    logging.info("%s:%s adding querystring filter",
                                 function_category_name, function_name)
                    function_out += get_querystring_filter(function)

                    # Enable adding the response function at the end
                    add_filter_querystring = True

                # Get payload
                if payload_exists(function):
                    logging.info("%s:%s adding payload",
                                 function_category_name, function_name)
                    function_out += get_payload(function)

                # Insert mid code
                if function_code_exists("mid", function):
                    logging.info("%s:%s adding mid code",
                                 function_category_name, function_name)
                    function_out += get_function_code("mid", function)

                if utils.key_exists("header", function):
                    logging.info("%s:%s adding http response",
                                 function_category_name, function_name)
                    function_out += get_http_response(function)

                # Insert the code to check the http response
                if check_http_response_exists(function):
                    logging.info("%s:%s adding check http response",
                                 function_category_name, function_name)
                    function_out += get_check_http_response(function)

                    # Enable adding the response function at the end
                    add_check_http_response = True

                # Insert end code
                if function_code_exists("end", function):
                    logging.info("%s:%s adding end code",
                                 function_category_name, function_name)
                    function_out += get_function_code("end", function)

                # Insert end code
                if return_exists(function):
                    logging.info("%s:%s adding return", function_category_name,
                                 function_name)
                    function_out += get_return(function)

                # Add to the all functions out array
                functions_out += function_out

    # Check if the checkHttpResponse function has been added yet
    if add_check_http_response:
        if not utils.key_exists("custom", config["functions"]):
            config["functions"]["custom"] = {}

        # If the code isn't there already
        if not utils.key_exists("checkHttpResponse",
                                config["functions"]["custom"]):
            # Not added, lets add it
            functions_out += get_check_http_response_function()

    # Check if the filterQuerystring function has been added yet
    if add_filter_querystring:
        if not utils.key_exists("custom", config["functions"]):
            config["functions"]["custom"] = {}

        # If the code isn't there already
        if not utils.key_exists("filterQuerystring",
                                config["functions"]["custom"]):
            # Not added, lets add it
            functions_out += get_querystring_filter_function()

    if utils.key_exists("main", config["functions"]):
        # Add main
        function_main = config["functions"]
        function = config["functions"]["main"]
        function_name = "main"
        logging.info("Building function %s", function_name)

        function_out = []
        # Function def and description
        function_out.append(
            utils.indent(
                f"def {function_name}({utils.get_parameters(function_main, function_name)}):",
                0))
        function_out.append(
            utils.indent(f"\"\"\"{function['description']}\"\"\"", 1))

        if utils.key_exists("code", function):
            if isinstance(function["code"], list):
                for line in function["code"]:
                    function_out.append(utils.indent(line, 1))
                function_out.append("")

        if utils.key_exists("run", function):
            function_out.append("")
            function_out.append("if __name__ == '__main__':")
            function_out.append(utils.indent("main()", 1))
            function_out.append("")

        functions_out += function_out

    return functions_out


def function_code_exists(level, function):
    """Determine if code exists in config"""

    if utils.key_exists("code", function):
        if isinstance(function["code"], list):
            # Must be a custom function
            return False
        # code exists, does the sub key?
        if utils.key_exists(level, function["code"]):
            logging.info("%s: Found %s code", level, function["name"])
            return True
    return False


def get_function_code(level, function, indent_level=2):
    """Get code from config"""

    if utils.key_exists("code", function):
        if utils.key_exists(level, function["code"]):
            logging.info("%s: Adding %s code %s LOC", level, function["name"],
                         len(function["code"][level]))
            code_out = []

            # Indent all the code
            for line in function["code"][level]:
                code_out.append(utils.indent(line, indent_level))
            return code_out
    return []


def querystring_exists(function):
    """Determine if querystring exists in config"""

    return utils.key_exists("querystring", function)


def get_querystring(function, indent_level=2):
    """Get querystring from config"""

    logging.info("%s: Getting querystring", function["name"])
    querystring_out = []
    querystring_out.append(utils.indent('querystring = {}', indent_level))

    if utils.key_exists("querystring", function):
        for querystring_name in function["querystring"]:
            querystring_func = function["querystring"][querystring_name]

            querystring_out.append(
                utils.generate_dictionary_variable_types(
                    "querystring", querystring_name, querystring_func,
                    indent_level))
        querystring_out.append("")
        return querystring_out

    return []


def payload_exists(function):
    """Determine if payload exists in config"""

    return utils.key_exists("payload", function)


def get_payload(function, indent_level=2):
    """Get payload from config"""

    logging.info("%s: Getting payload", function["name"])
    payload_out = []
    payload_out.append(utils.indent('payload = {}', indent_level))

    if utils.key_exists("payload", function):
        for payload_name in function["payload"]:
            payload_func = function["payload"][payload_name]

            payload_out.append(
                utils.generate_dictionary_variable_types(
                    "payload", payload_name, payload_func, indent_level))
        payload_out.append("")
        return payload_out
    return []


def get_http_response(function):
    """Make response from config"""

    http_response_out = []
    http_function = function["header"]
    method = function["method"]
    path = function["path"]

    if utils.key_exists("querystring", function):
        querystring = ', querystring=querystring'
    else:
        querystring = ""

    if utils.key_exists("payload", function):
        payload = ', payload=payload'
    else:
        payload = ""

    http_response_out.append(
        utils.indent(
            f'response = self.{http_function}.{method}(f"{path}"{querystring}{payload})',
            2))

    http_response_out.append("")

    return http_response_out


def check_http_response_exists(function):
    """Determine if response exists in config"""

    return utils.key_exists("checkHttpResponse", function)


def querystring_filter_exists(function):
    """Determine if querystring_filter exists in config"""

    return utils.key_exists("filterQuerystring", function)


def get_check_http_response(function):
    """Get checkHttpResponse from config"""

    if utils.key_exists("checkHttpResponse", function):
        logging.info("%s: Adding http response code", function["name"])

        if function["checkHttpResponse"]:
            # If a specific code is expected the inject it to the check
            if utils.key_exists("expectedHttpCode", function):
                expected_http_code = ", " + str(function["expectedHttpCode"])
            else:
                expected_http_code = ""

            code = [
                "        if self.check_http_response(response%s):" %
                expected_http_code,
                "            return json.loads(response.text)",
                "        else:",
                "            logging.error('Error with HTTP request')",
                "            return False", ""
            ]

            return code
    return []


def get_querystring_filter(function):
    """Get filterQuerystring from config"""

    # If filterQuerystring present then add the function in custom functions
    if utils.key_exists("filterQuerystring", function):
        logging.info("%s: Adding querystring filter code", function["name"])

        if function["filterQuerystring"]:
            code = [
                "        querystring = self.filter_querystring(querystring)",
                ""
            ]

            return code
    return []


def return_exists(function):
    """Determine if return exists in config"""

    return utils.key_exists("return", function)


def get_return(function, indent_level=2):
    """Get return from config"""

    if utils.key_exists("return", function):
        return [utils.indent(f'return {function["return"]}', indent_level)]
    return []


def get_check_http_response_function():
    """Returns the function for checking the http response"""
    logging.info("Creating checkHttpResponse custom function")

    get_check_http_response_function_list = [
        "    def check_http_response(self, response, expected_code=None):",
        '        """Checks if response is a expected or a known good response"""',
        "    ", "        status_codes = {}",
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
        "", '        # Check if a HTTP code is a "good" code',
        "        if response.status_code == expected_code:",
        "            return True", "    ",
        "        # Lookup the code in the dict",
        "        elif response.status_code in status_codes:",
        "            logging.debug(status_codes[response.status_code][1])",
        "            if response.status_code != 200:",
        "                # Show the body for non 200",
        "                logging.debug(response.text)",
        "            return status_codes[response.status_code][0]", "",
        "        # Unable to find code return False", "        else:",
        "            logging.error('Unknown code %s', response.status_code)",
        "            return False", ""
    ]

    return get_check_http_response_function_list


def get_querystring_filter_function():
    """Returns the function for filtering querystrings"""

    logging.info("Creating querystring filtering function")

    filter_querystring_list = [
        "    def filter_querystring(self, querystring):",
        '        """Removes None value keys from the querystring"""',
        "",
        "        querystring_out = {}",
        "        for key in querystring:",
        "            if querystring[key] != None:",
        "                querystring_out[key] = querystring[key]",
        "",
        "        return querystring_out",
    ]

    return filter_querystring_list
