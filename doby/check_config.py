import os
import sys
import logging
import json

logging.getLogger().setLevel(logging.INFO)


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

    return config, override_config


class check_keys:
    def __init__(self, filename) -> None:
        self.config, self.override_config = load_config(filename)

    def check_keys_in_dict(self, config, override_config, required_keys):
        for required_key in required_keys:
            if (
                required_key not in config.keys()
                and required_key not in override_config.keys()
            ):
                logging.error("%s required in config" % (required_key))

    def check_optional_keys_in_dict(
        self, config, override_config, required_keys, optional_keys, path
    ):
        for key in config.keys():
            if key not in required_keys and key not in optional_keys:
                logging.error("%s: Unknown key %s" % (path, key))

        for key in override_config.keys():
            if key not in required_keys and key not in optional_keys:
                logging.error("%s: Unknown key %s" % (path, key))

    def check_function_variable_static(self, config, path):
        allowed = ["function", "variable", "static"]

        for header in config.keys():
            for key in config[header]:
                if key not in allowed:
                    logging.error("%s:%s:%s Unknown key %s" % (path, header, key, key))
                else:
                    logging.info(
                        "%s:%s:%s key is %s"
                        % (path, header, key, type(config[header][key]))
                    )
                # Logging info? TODO

    def check_type(self, config, override_config, key, path):
        if key in config.keys():
            return type(config[key])
        elif key in override_config:
            return type(override_config[key])
        else:
            return None

    def check_key_both(self, config, override_config, key, path, optional=False):

        if optional:
            optional_str = "optional "
        else:
            optional_str = ""

        if key in config.keys():
            logging.info(
                "%s:%s %skey exists in config file" % (path, key, optional_str)
            )
            return True
        elif key in override_config.keys():
            logging.info(
                "%s:%s %skey exists in override config file" % (path, key, optional_str)
            )
            return True
        else:
            if optional:
                logging.warning(
                    "%s:%s %skey doesn't exist in either config file"
                    % (path, key, optional_str)
                )
            else:
                logging.error(
                    "%s:%s %skey doesn't exist in either config file"
                    % (path, key, optional_str)
                )
            return False

    def think_of_a_better_name(
        self, config, override_config, key, path, expected_type, optional
    ) -> bool:

        # If the key exists in either config
        if self.check_key_both(config, override_config, key, path, optional):

            # If it exists is it the right type
            if self.check_type(config, override_config, key, path) == expected_type:
                logging.info("%s:%s is correct type", path, key)
                return True
            else:
                logging.error("%s:%s should be a %s", path, key, expected_type)
                return False
        # Doesn't exist
        return False

    def check_top_level(self):

        required_keys = ["name", "description", "hostname", "headers", "functions"]
        optional_keys = ["debug", "requirements", "setup", ".gitignore", "override"]

        # Check all higher level keys
        self.check_keys_in_dict(self.config, self.override_config, required_keys)

        self.check_optional_keys_in_dict(
            self.config, self.override_config, required_keys, optional_keys, "."
        )

    def check_name(self):
        """Check the name keys"""

        key = "name"
        path = "."
        expected_type = str
        optional = False

        self.think_of_a_better_name(
            self.config, self.override_config, key, path, expected_type, optional
        )

    def check_description(self):
        """Check the description keys"""

        key = "description"
        path = "."
        expected_type = str
        optional = False

        self.think_of_a_better_name(
            self.config, self.override_config, key, path, expected_type, optional
        )

    def check_debug(self):
        """Check the debug keys"""

        key = "debug"
        path = "."
        expected_type = bool
        optional = True

        self.think_of_a_better_name(
            self.config, self.override_config, key, path, expected_type, optional
        )

    def check_requirements(self):
        """Check the requirements keys"""

        key = "requirements"
        path = "."
        expected_type = dict
        optional = True

        if self.think_of_a_better_name(
            self.config, self.override_config, key, path, expected_type, optional
        ):

            if key in self.config:
                for requirement in self.config[key]:
                    if self.config[key][requirement] == {}:
                        logging.info(
                            "%s:%s:%s is a valid requirement", path, key, requirement
                        )
                    else:
                        optional_keys = ["operator", "version", "builtin"]

                        self.check_optional_keys_in_dict(
                            self.config[key][requirement], {}, [], optional_keys, "."
                        )

            elif key in self.override_config:
                for requirement in self.override_config[key]:
                    if self.override_config[key][requirement] == {}:
                        logging.info(
                            "%s:%s:%s is a valid requirement", path, key, requirement
                        )
                    else:
                        optional_keys = ["operator", "version", "builtin"]

                        self.check_optional_keys_in_dict(
                            {},
                            self.override_config[key][requirement],
                            [],
                            optional_keys,
                            ".",
                        )

        # TODO check requirments

    def check_hostname(self):
        """Check the hostname keys"""

        key = "hostname"
        path = "."
        expected_type = dict
        optional = True

        self.think_of_a_better_name(
            self.config, self.override_config, key, path, expected_type, optional
        )

        # TODO check hostname

    def check_headers(self):
        """Check the headers keys"""

        key = "headers"
        path = "."
        expected_type = dict
        optional = False

        if self.think_of_a_better_name(
            self.config, self.override_config, key, path, expected_type, optional
        ):
            if key in self.config:
                for header in self.config[key]:
                    self.check_function_variable_static(
                        self.config[key][header], ".:headers:" + header
                    )

            elif key in self.override_config:
                for header in self.override_config[key]:
                    self.check_function_variable_static(
                        self.override_config[key][header], ".:headers:" + header
                    )

        # TODO check headers

    def check_functions(self):
        """Check the functions keys"""

        key = "functions"
        path = "."
        expected_type = dict
        optional = False

        return self.think_of_a_better_name(
            self.config, self.override_config, key, path, expected_type, optional
        )

    def check_init_functions(self):
        """Check the init_functions keys"""

        key = "init"
        path = ".:functions"
        expected_type = dict
        optional = True

        self.think_of_a_better_name(
            self.config["functions"],
            self.override_config["functions"],
            key,
            path,
            expected_type,
            optional,
        )

    def check_main_functions(self):
        """Check the main_functions keys"""

        key = "main"
        path = ".:functions"
        expected_type = dict
        optional = True

        self.think_of_a_better_name(
            self.config["functions"],
            self.override_config["functions"],
            key,
            path,
            expected_type,
            optional,
        )

    def check_endpoint_functions(self):
        """Check the endpoint_functions keys"""

        key = ".:endpoint"
        path = "functions"
        expected_type = dict
        optional = False

        self.think_of_a_better_name(
            self.config["functions"],
            self.override_config["functions"],
            key,
            path,
            expected_type,
            optional,
        )

    def check_custom_functions(self):
        """Check the custom_functions keys"""

        key = ".:custom"
        path = "functions"
        expected_type = dict
        optional = True

        self.think_of_a_better_name(
            self.config["functions"],
            self.override_config["functions"],
            key,
            path,
            expected_type,
            optional,
        )

    def check_setup_py(self):
        """Check the setup_py keys"""

        key = "setup"
        path = "."
        expected_type = dict
        optional = True

        self.think_of_a_better_name(
            self.config, self.override_config, key, path, expected_type, optional
        )

        # TODO check setup

    def check_gitignore(self):
        """Check the gitignore keys"""

        key = ".gitignore"
        path = "."
        expected_type = list
        optional = True

        self.think_of_a_better_name(
            self.config, self.override_config, key, path, expected_type, optional
        )

        # TODO check headers

    #     # Check all higher level keys

    #     for required_key in required_keys:
    #         if required_key not in config_dict.keys() and required_key not in override_config_dict.keys():
    #             logging.error("%s required in config" % (required_key))

    #     for key in config_dict.keys():
    #         if key not in required_keys and key not in optional_keys:
    #             logging.error("%s: Unknown key %s" % ("config", key))

    #     for key in override_config_dict.keys():
    #         if key not in required_keys and key not in optional_keys:
    #             logging.error("%s: Unknown key %s" % ("override_config", key))


def main():
    cc = check_keys("configs/wso.json")

    cc.check_top_level()
    cc.check_name()
    cc.check_description()
    cc.check_debug()
    cc.check_requirements()
    cc.check_hostname()
    cc.check_headers()
    if cc.check_functions():
        cc.check_init_functions()
        cc.check_main_functions()
        cc.check_endpoint_functions()
        cc.check_custom_functions()
    cc.check_setup_py()
    cc.check_gitignore()

    print("Check completed")


if __name__ == "__main__":
    main()
