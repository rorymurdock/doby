"""Doby config normalise"""
import re
import logging


def safe_variable(input_str):
    """Remove certain special characters from string"""

    elemnts = ["{", "}", "-", ":", "."]
    for elemnt in elemnts:
        input_str = input_str.replace(elemnt, "")

    return input_str


def path(input_str, skip_caps=False):
    """Remove certain special characters from string"""
    elemnts = ["/", "{", "}", "-", ":", "."]
    for elemnt in elemnts:
        input_str = input_str.replace(elemnt, "")

    if not skip_caps:
        input_str = input_str.capitalize()

    # logging.info("Normalised string")
    return input_str


def dynamic_path(input_str):
    """Normalise dynamic paths"""
    # Not needed at the moment
    return input_str


def version(produces: list):
    """Find the version"""

    for produced in produces:
        if "application/json" in produced:
            re_version = re.search(r"version=(.*)", produced)
            if re_version is not None:
                logging.info("API version %s found", re_version.group(1))
                return int(re_version.group(1))

    logging.error("Unable to find version: %s", produces)
    logging.warning("Defaulting to API v1")
    return 1  # default to API version 1


def normalise_type(type_string):
    """Normalise the argument type"""

    type_map = {}
    type_map[""] = "str"
    type_map["uuid"] = "str"
    type_map["String"] = "str"
    type_map["string"] = "str"
    type_map["None"] = "str"
    type_map["int32"] = "int"
    type_map["integer"] = "int"
    type_map["boolean"] = "bool"

    if type_string in type_map:
        logging.info("Normalised %s to %s", type_string, type_map[type_string])
        return type_map[type_string]
    print("Error: type %s not in normalisation map" % type_string)
    return "str"
