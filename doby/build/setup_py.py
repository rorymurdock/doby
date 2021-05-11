"""Doby class build testing"""
import logging
from doby import utils
from doby.build import imports


def build_setup(config):
    """Build the setup.py file"""
    if not utils.key_exists("setup", config):
        logging.error("Setup build called without a setup key")
        return ""

    for required_key in ["version", "author", "author_email", "url"]:
        if not utils.key_exists(required_key, config["setup"]):
            logging.error("Field %s is missing in setup dict")
            return ""

    setup_parameters = "version = \"%s\"" % config["setup"]["version"]
    setup_parameters += ", author = \"%s\"" % config["setup"]["author"]
    setup_parameters += ", author_email = \"%s\"" % config["setup"][
        "author_email"]
    setup_parameters += ", url = \"%s\"" % config["setup"]["url"]
    setup_parameters += ", description = \"%s\"" % config["description"]
    setup_parameters += ", long_description=LONG_DESCRIPTION"
    setup_parameters += ", long_description_content_type=\"text/markdown\""

    setup_parameters += "classifiers=["

    if utils.key_exists("developmentStatus", config["setup"]):
        setup_parameters += "\"Development Status :: %s\"," % config["setup"][
            "developmentStatus"]

    if utils.key_exists("license", config["setup"]):
        setup_parameters += "\"License Status :: %s\"," % config["setup"][
            "license"]

    if utils.key_exists("operatingSystem", config["setup"]):
        setup_parameters += "\"Operating System :: %s\"," % config["setup"][
            "operatingSystem"]

    if utils.key_exists("pythonVersion", config["setup"]):
        setup_parameters += "\"Programming Language :: %s\"," % config[
            "setup"]["pythonVersion"]

    setup_parameters += "]"

    setup_parameters += ", install_requires=%s" % imports.get_clean_non_built_ins(
        config)
    setup_parameters += ", include_package_data=True"

    setup_out = []
    setup_out.append('import setuptools')
    setup_out.append('')
    setup_out.append('with open("README.md", "r") as fh:')
    setup_out.append('    LONG_DESCRIPTION = fh.read()')
    setup_out.append('')
    setup_out.append('setuptools.setup(%s)' % setup_parameters)

    return setup_out
