"""Doby import build testing"""
import logging
from doby import utils


def build_import(config):
    """Get the required packages and make requirements and import lists"""

    if "requirements" in config.keys():
        requirements = config["requirements"]
    else:
        requirements = {}
    logging.info("Generating imports: %i", len(requirements))

    # Create arrays
    requirement_list = ["requests"]
    import_list = ["import logging", "import requests"]

    for requirement in requirements:
        # Add each import into file imports
        logging.info("Adding %s to imports", requirement)
        import_list.append(f"import {requirement}")

        if utils.key_exists_get_value("builtin", requirements[requirement]):
            # Built in don't need adding to requirements.txt
            # TODO allow requests version pinning
            logging.info("%s is built in", requirement)
        else:
            # Combine all the strings (if not None)
            if all([
                    utils.key_exists("operator", requirements[requirement]),
                    utils.key_exists("version", requirements[requirement]),
            ]):
                pinned_requirement = (requirement +
                                      requirements[requirement]["operator"] +
                                      requirements[requirement]["version"])
                logging.info("Adding pinned dependency %s to requirements",
                             pinned_requirement)
                requirement_list.append(pinned_requirement)
            else:
                # Add just the name
                logging.info("Adding dependency %s to requirements",
                             requirement)
                requirement_list.append(requirement)

    # Add extra line for formatting
    import_list.append("")

    return requirement_list, import_list


def get_clean_non_built_ins(config):
    """Returns a list of non built in functions"""
    logging.info("Generating clean non built-in imports")

    # Create arrays
    requirement_list = ["reqrest"]

    for requirement in config["requirements"]:
        if not utils.key_exists_get_value("builtin",
                                          config["requirements"][requirement]):
            # Not built in
            requirement_list.append(requirement)

    return requirement_list
