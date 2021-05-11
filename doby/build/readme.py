"""Doby README build testing"""
import logging
from doby import utils


def build_readme(config):
    """Build the readme in markdown"""

    readme = []
    readme.append("# %s" % config["name"])
    readme.append("")
    readme.append(config["description"])
    readme.append("")
    readme.append("## Default functions")
    readme.append("")
    for function_name in ["init", "main"]:
        if utils.key_exists(function_name, config["functions"]):
            logging.info("Adding %s to readme", function_name)
            readme += format_function(function_name, config["functions"])

    for function_category_name in ["endpoint", "custom"]:
        if utils.key_exists(function_category_name, config["functions"]):
            logging.info("Adding category%s to readme", function_category_name)
            readme.append("## %s functions" %
                          function_category_name.capitalize())
            readme.append("")
            for function_name in config["functions"][function_category_name]:
                logging.info("Adding %s to readme", function_name)
                readme += format_function(
                    function_name, config["functions"][function_category_name])

    return readme


def format_function(name, function):
    """Format the function details for markdown"""

    # Remap the function
    function = function[name]

    # Create the array to append and return
    function_out = []

    # Function name
    if utils.key_exists("name", function):
        function_out.append("### %s()" % function["name"])
    else:
        function_out.append("### %s()" % name)
    function_out.append("")

    # Add description
    if utils.key_exists("description", function):
        function_out.append(function["description"])
        function_out.append("")

    if utils.key_exists("parameters", function):
        if len(function["parameters"]) > 0:
            # Create Table
            function_out.append("|Name|Description|Type|Default value|")
            function_out.append("|-|-|-|-|")

            for parameter in function["parameters"]:
                param_row = "|"
                # Add param name
                param_row += "%s|" % parameter

                # Add description
                if utils.key_exists("description",
                                    function["parameters"][parameter]):
                    param_row += "%s|" % function["parameters"][parameter][
                        "description"]
                else:
                    param_row += "|"

                # Add type
                if utils.key_exists("type", function["parameters"][parameter]):
                    param_row += "%s|" % function["parameters"][parameter][
                        "type"]
                else:
                    param_row += "|"

                # Add default value
                if utils.key_exists("defaultValue",
                                    function["parameters"][parameter]):
                    param_row += "%s|" % function["parameters"][parameter][
                        "defaultValue"]
                else:
                    param_row += "|"

                function_out.append(param_row)
            function_out.append("")

    # Add return
    if utils.key_exists("returns", function):
        function_out.append("Returns: `%s`" % function["returns"])
        function_out.append("")

    # Add checkHttpResponse
    if utils.key_exists("checkHttpResponse", function):
        if function["checkHttpResponse"]:
            function_out.append("The response will be checked")

        function_out.append("")

    if utils.key_exists("run", function):
        function_out.append("This function will run if launched directly")
        function_out.append("")

    return function_out
