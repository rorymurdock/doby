def create_directories(self):
    """Create required directories"""
    for directory in [self.output_dir, self.config_output_dir]:
        if not os.path.isdir(directory):
            os.mkdir(directory)

def read_swagger_files(self):
    """Read the swagger file"""
    swagger_files = []
    for json_file in os.listdir(self.output_dir):
        if ".json" in json_file:
            print(json_file)
            with open(self.output_dir + "/" + json_file) as read_file:
                swagger_files.append(json.load(read_file))

    return swagger_files

def normalise_name(self, name, skip_caps=False):
    """Remove certain special characters from string"""
    elemnts = ["/", "{", "}", "-", ":", "."]
    for elemnt in elemnts:
        name = name.replace(elemnt, "")

    if not skip_caps:
        name = name.capitalize()
    return name

def get_description(self, definition):
    """Get the description from a function definition"""
    # Alt definition["summary"]
    if "description" in definition.keys():
        return definition["description"]
    return ""

def get_parameters(self, definition):
    """Get parameters from a function definition"""
    params_out = {}

    if "parameters" not in definition.keys():
        return {}

    for param in definition["parameters"]:
        param_out = {}
        # Resolve meta refs
        if "$ref" in param.keys():
            path = param["$ref"].split("/")
            del path[0]
            print(path)
            val = self.definition
            for nested_key in path:
                val = val[nested_key]
            print(val)
            param = val
            # continue

        if "description" not in param.keys():
            print("Warning: No description for %s" % param["name"])
            param_out["description"] = ""
            continue

        # param["default"] # TODO find out what this is for
        param_out["description"] = param["description"]
        param_out["name"] = param["name"]

        try:
            if param["required"] is False:
                param_out["defaultValue"] = "None"
        except KeyError:
            param_out["defaultValue"] = "None"

        try:
            param_out["type"] = self.normalise_type(param["type"])
        except KeyError:
            pass

        params_out[param["name"]] = param_out

    return params_out

def find_parameter_refs(self, definition):
    """Resolve internal parameter links"""
    params_out = {}

    for param in definition["parameters"]:
        if "$ref" in param.keys():
            path = param["$ref"].split("/")
            del path[0]
            print(path)
            val = self.definition
            for recursive_key in path:
                val = val[recursive_key]
            print(val)
            param = val
        params_out[self.normalise_name(param["name"].lower())] = param

    return params_out

def normalise_type(self, type_string):
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
            return type_map[type_string]
        else:
            print("Error: type %s not in map" % type_string)
            return "str"

    def store_definition(self, definition):
        """Store a definition"""
        self.definition = definition

    def write_config(self, config):
        """Write the config to file"""
        filename = self.config_output_dir + "/" + self.output_file + ".json"
        print("writing config to %s" % filename)
        with open(filename, "w", encoding="utf8") as output:
            json.dump(config, output, indent=4)
