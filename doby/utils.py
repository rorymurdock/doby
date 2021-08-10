"""Doby utilities"""
import os
import logging
import subprocess


def get_debug(debug: bool, config_dict: dict, override_config_dict: dict):
    """Finds if debug is enabled in arg or config files"""
    logging.debug("Checking if debugging is enabled")

    config_dict_debug = False
    override_config_dict_debug = False

    if key_exists("debug", config_dict):
        config_dict_debug = config_dict["debug"]

    if key_exists("debug", override_config_dict):
        override_config_dict_debug = override_config_dict["debug"]

    logging.debug(
        "Debugging: %s", any((debug, config_dict_debug, override_config_dict_debug))
    )
    return any((debug, config_dict_debug, override_config_dict_debug))


def key_exists(search_key: str, search_dict: dict):
    """Returns bool if a key exists at the top level of a dict"""

    return search_key in search_dict.keys()


def key_exists_get_value(search_key: str, search_dict: dict):
    """Returns bool if a key exists at the top level of a dict"""

    if key_exists(search_key, search_dict):
        return search_dict[search_key]
    return False


def write_list_to_file(filename, path, data, no_new_line=False):
    """Writes str to file"""

    logging.info("Writing to %s/%s: %s lines", path, filename, len(data))
    if not os.path.exists(path):
        logging.info("Creating %s directory", path)
        os.mkdir(path)

    with open("%s/%s" % (path, filename), "a", encoding="utf8") as write_file:
        for line in data:
            write_file.write(line + ("" if no_new_line else "\n"))


def write_to_file(filename, path, data, no_new_line=False):
    """Writes str to file"""

    logging.info("Writing to %s%s: %s char", path, filename, len(data))
    if not os.path.exists(path):
        logging.info("Creating %s directory", path)
        os.mkdir(path)

    with open("%s/%s" % (path, filename), "a", encoding="utf8") as write_file:
        write_file.write(data + ("" if no_new_line else "\n"))


def indent(string_in: str, tabs: int = 0):
    """Returns the str intended using spaces"""

    return str("    " * tabs) + string_in


def get_parameters(functions: dict, function_name):
    """Parse the paramaters, format them for the function"""

    # One var per parameter type
    standard_parameter_out = ""
    type_parameter_out = ""
    default_parameter_out = ""
    type_default_parameter_out = ""

    # Don't escape these:
    types_used = ["None", "True", "False", None, True, False, "{}"]

    # No args, return empty str
    if not key_exists("parameters", functions[function_name]):
        logging.info("%s: No parameters", function_name)
        return ""

    # Go through each arg and see if it has a type and/or default
    for parameter_name in functions[function_name]["parameters"]:
        logging.info("%s: Adding parameter %s", function_name, parameter_name)
        parameter_dict = functions[function_name]["parameters"][parameter_name]

        # Type and default
        if key_exists("type", parameter_dict) and key_exists(
            "defaultValue", parameter_dict
        ):
            logging.info(
                "%s: %s has type %s and defaultValue of %s",
                function_name,
                parameter_name,
                parameter_dict["type"],
                parameter_dict["defaultValue"],
            )

            if (
                parameter_dict["type"] == "int"
                or parameter_dict["defaultValue"] in types_used
            ):
                type_default_parameter_out += ", %s: %s = %s" % (
                    parameter_name,
                    parameter_dict["type"],
                    parameter_dict["defaultValue"],
                )
            else:
                type_default_parameter_out += ', %s: %s = "%s"' % (
                    parameter_name,
                    parameter_dict["type"],
                    parameter_dict["defaultValue"],
                )

        # Type only
        elif key_exists("type", parameter_dict):
            logging.info(
                "%s: %s has type %s",
                function_name,
                parameter_name,
                parameter_dict["type"],
            )
            type_parameter_out += ", %s: %s" % (parameter_name, parameter_dict["type"])

        # Default only
        elif key_exists("defaultValue", parameter_dict):
            logging.info(
                "%s: %s has defaultValue of %s",
                function_name,
                parameter_name,
                parameter_dict["defaultValue"],
            )

            if parameter_dict["defaultValue"] in types_used:
                default_parameter_out += ", %s = %s" % (
                    parameter_name,
                    parameter_dict["defaultValue"],
                )
            else:
                default_parameter_out += ', %s = "%s"' % (
                    parameter_name,
                    parameter_dict["defaultValue"],
                )

        # Just a std arg
        else:
            logging.info("%s: %s added", function_name, parameter_name)
            standard_parameter_out += ", %s" % parameter_name

    # A little messy but combines the var types in order so you don't get defaults before non defaults
    return (
        standard_parameter_out
        + type_parameter_out
        + default_parameter_out
        + type_default_parameter_out
    )


def generate_dictionary_variable_types(
    dict_name, key_name, search_dict, indent_level=0
):
    """Generate a dictionary from config with values from either function, variable, or static"""

    out_str = []
    # Don't escape these:
    types_used = ["None", "True", "False", None, True, False]

    if len(search_dict) < 1:
        logging.warning("Can't search 0 len dict")
        return None

    if key_exists("function", search_dict):
        logging.info("Found funciton in dict")
        out_str = f'{dict_name}["{key_name}"] = {search_dict["function"]}'
    elif key_exists("variable", search_dict):
        logging.info("Found variable in dict")
        out_str = f'{dict_name}["{key_name}"] = {search_dict["variable"]}'
    elif key_exists("static", search_dict):
        if (
            isinstance(search_dict["static"], int)
            or search_dict["static"] in types_used
        ):
            logging.info("Found static (None / Bool) in dict")
            out_str = f'{dict_name}["{key_name}"] = {search_dict["static"]}'
        else:
            logging.info("Found static (string) in dict")
            out_str = f'{dict_name}["{key_name}"] = "{search_dict["static"]}"'
    else:
        logging.warning("Unable to find function, variable, or static string")
        return None

    return indent(out_str, indent_level)


def get_variable_keys_value_only(search_dict):
    """If the key exists return it's value"""

    # Don't escape these:
    types_used = [None, True, False]
    convert_dict = {"True": True, "False": False, "None": None}

    if key_exists("function", search_dict):
        logging.info("Found function in dict")
        return search_dict["function"]

    if key_exists("variable", search_dict):
        logging.info("Found variable in dict")
        return search_dict["variable"]

    if key_exists("static", search_dict):
        if search_dict["static"] in convert_dict:
            logging.info("Found static (None / Bool) in dict")
            return convert_dict[search_dict["static"]]
        elif (
            isinstance(search_dict["static"], int)
            or search_dict["static"] in types_used
        ):
            logging.info("Found static (None / Bool) in dict")
            return search_dict["static"]
        else:
            logging.info("Found static in dict")
            return f'"{search_dict["static"]}"'
    logging.warning("Unable to find function, variable, or static string")
    return ""


def clear_export_directory(directory="exports/"):
    """Deletes all files & folders in the export directory"""

    logging.info("Clearing existing export directory: %s", directory)

    if "../" in directory:
        logging.error("Deleting directories beyond current WD not supported")
        return False

    if not os.path.exists(directory):
        return False

    return subprocess.run(["rm", "-rf", directory], check=True)
