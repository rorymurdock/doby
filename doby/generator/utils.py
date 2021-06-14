"""Doby generator utils"""
import logging


def get_description(definition):
    """Get the description from a function definition"""

    # Alt definition["summary"]
    if "description" in definition.keys():
        logging.info("Found description")
        return definition["description"]

    if "summary" in definition.keys():
        logging.info("Using summary for description")
        return definition["summary"]

    logging.warning("Unable to find description")
    return ""
