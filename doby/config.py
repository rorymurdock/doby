"""Doby config"""
import os
import sys
import json
import logging
from .utils import key_exists


def load_config(config_filename):
    """Load the config files merge them and return it"""

    override_config_filename = config_filename.replace(".json", "_override.json")
    logging.info("config_file: %s", config_filename)
    logging.info("override_file: %s", override_config_filename)

    try:
        logging.info("Importing config from %s", config_filename)
        # Import the configs
        if os.path.isfile(config_filename):
            with open(config_filename) as read_file:
                config = json.load(read_file)
            logging.info("Successfully imported %s for config", config_filename)
        else:
            logging.critical("File %s doesn't exist, exiting", config_filename)
            sys.exit()

        # Import the override file if it exists
        logging.info("Importing override config from %s", override_config_filename)
        if os.path.isfile(override_config_filename):
            with open(override_config_filename) as read_file:
                override_config = json.load(read_file)
            logging.info(
                "Successfully imported %s for override config", config_filename
            )
        else:
            logging.warning("No override file found: %s", override_config_filename)
            # Set an empty-ish dict
            override_config = {"override": False}

    except json.JSONDecodeError as error:
        # JSON is malformed, can't continue
        logging.critical("Unable to parse JSON config file: %s", error)
        sys.exit()

    return walk(config, override_config)


def walk(config, override):
    """Walks through the override config and merges into main config"""

    logging.basicConfig(
        format="%(levelname)s	%(funcName)s	%(message)s", level=logging.INFO
    )
    for override_key, override_value in override.items():
        # If the value is another dictionary go deeper
        if isinstance(override_value, dict):

            if key_exists(override_key, config):
                # If this key exists go deeper
                logging.debug("mergeConfig: nested key - %s", override_key)
                walk(config=config[override_key], override=override_value)
            else:
                # The key doesn't exist in config, make it, the go deeper
                logging.debug("mergeConfig: Creating key %s", override_key)
                config[override_key] = {}
                walk(config=config[override_key], override=override_value)
        else:
            # We've hit a value that config has, overwrite it
            logging.debug("mergeConfig: %s has an override", override_key)
            if not key_exists(override_key, config):
                # Key doesn't exist, log differently
                logging.debug(
                    'mergeConfig: Adding ["%s"]: %s', override_key, override_value
                )
            else:
                logging.debug(
                    'mergeConfig: Replacing ["%s"]: %s with ["%s"]: %s',
                    override_key,
                    config[override_key],
                    override_key,
                    override_value,
                )

            config[override_key] = override_value

    return config
