"""Doby function testing"""
from doby import Doby
from . import test_config

config_filename = test_config.write_config(test_config.create_test_config())

DOBY = Doby(config_filename=config_filename, debug=True)

# def test_get_and_write_output():
#     """Used to write output of the build function"""
#     DOBY.reset_config(test_config.create_test_all_config())
#     from doby.utils import write_to_file

#     write_to_file("test_output.txt", ".", str(DOBY.build_file()))


def test_build_file():
    """Test building a whole library"""

    DOBY.reset_config(test_config.create_test_all_config())
    assert DOBY.build_file() == {
        "PyTest/PyTest.py": [
            '"""File automatically generated by Doby - https://github.com/rorymurdock/doby"""',
            "import logging",
            "import requests",
            "import os",
            "import panda",
            "",
            "class PyTest():",
            '    """PyTest configuration library"""',
            "    def __init__(self, debug: bool = False):",
            '        """Class init"""',
            "",
            "        # Init code from config",
            "",
            "        # rest headers",
            "        self.rest = {}",
            '        self.rest["Accept"] = "application/json"',
            '        self.rest["api-key"] = get_api_key()',
            "        ",
            "",
            "        # Requests variables",
            "        self.hostname = get_url()",
            "        self.debug = debug",
            "",
            "    def systemInfo(self, pagesize: int = 500, page: int = 0):",
            '        """Gets System information"""',
            "",
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
            '        response = requests.get(f"https://{self.hostname}/api/system/info", headers=self.rest, params=querystring, data=payload)',
            "",
            "        if self.check_http_response(response):",
            "            return json.loads(response.text)",
            "        else:",
            "            logging.error('Error with HTTP request')",
            "            return False",
            "",
            "    def custom_test(self, pagesize: int = 500):",
            '        """Custom test description"""',
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
            "def main():",
            '    """This is the main function"""',
            "    uem = WSO()",
            '    print(uem.systemInfo()["ProductVersion"])',
            "",
            "",
            "if __name__ == '__main__':",
            "    main()",
            "",
        ],
        "requirements.txt": ["requests", "panda==1.0.0"],
        ".gitignore": ["*.pyc"],
        "README.md": [
            "# PyTest",
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
            "## Custom functions",
            "",
            "### custom_test()",
            "",
            "Custom test description",
            "",
            "|Name|Description|Type|Default value|",
            "|-|-|-|-|",
            "|pagesize|How many results to return|int|500|",
            "",
        ],
        "setup.py": [
            "import setuptools",
            "",
            'with open("README.md", "r") as fh:',
            "    LONG_DESCRIPTION = fh.read()",
            "",
            'setuptools.setup(name="PyTest", version="1.0.0", author="Me", author_email="me@example.com", url="https://example.com", description="PyTest configuration library", long_description=LONG_DESCRIPTION, long_description_content_type="text/markdown", classifiers=[], install_requires=[\'reqrest\', \'panda\'], include_package_data=True)',
        ],
    }
