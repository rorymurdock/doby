"""Doby class build testing"""
import logging
from doby import utils


def build_class(config):
    """Build a class from config"""

    logging.info("Generating class: %s", config["name"])

    # Create the class for the lib
    class_out = [utils.indent("class %s():" % config["name"])]
    class_out.append(utils.indent('"""%s"""' % config["description"], 1))
    class_out.append(
        utils.indent("def __init__(self%s):" % get_class_parameters(config),
                     1))

    class_out.append(utils.indent('"""Class init"""', 2))
    class_out.append("")

    if utils.key_exists("init", config["functions"]):
        if utils.key_exists("code", config["functions"]["init"]):
            class_out.append(utils.indent("# Init code from config", 2))
            for line in config["functions"]["init"]["code"]:
                class_out.append(utils.indent(line, 2))

    class_out.append("")
    class_out += get_headers(config, 2)
    class_out.append("")
    class_out += get_http_response_function(config, 2)
    class_out.append("")

    return class_out


def get_class_parameters(config):
    """Get paratemers for the  class __init__"""

    logging.info("Generating class pamaters: %s", config["name"])
    if utils.key_exists("init", config["functions"]):
        return utils.get_parameters(config["functions"], "init")
    return ""


def get_headers(config, indent_level=2):
    """Get headers to add to init"""
    header_out = []

    if utils.key_exists("headers", config):
        for header_name in config["headers"]:
            header_out.append(
                utils.indent(f"# {header_name} headers", indent_level))
            header_out.append(
                utils.indent(f"{header_name} = {{}}", indent_level))
            for header_item in config["headers"][header_name]:

                header_out.append(
                    utils.indent(
                        utils.generate_dictionary_variable_types(
                            header_name, header_item,
                            config["headers"][header_name][header_item]),
                        indent_level))

            header_out.append(utils.indent("", indent_level))

    return header_out


def get_http_response_function(config, indent_level=2):
    """Create a http function for each header"""
    response_out = []
    debug = config['debug']
    if utils.key_exists("headers", config):
        response_out.append(utils.indent("# REST Functions", 2))
        for header_name in config["headers"]:
            hostname = utils.get_variable_keys_value_only(config["hostname"])
            response_out.append(
                utils.indent(
                    f"self.{header_name} = reqrest.REST(url={hostname}, debug={debug}, headers={header_name})",
                    indent_level))

    return response_out
