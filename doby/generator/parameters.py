"""Doby config parameters"""
import logging
from .normalise import normalise_type, safe_variable


def querystring(parameters):
    """Generate the querystring from parameters"""

    logging.info("Generating querystring")

    querystring_out = {}

    for parameter in parameters:
        if "in" in parameter.keys():
            if parameter["in"] == "query":
                name = parameter["name"]
                querystring_out[name] = {}

                querystring_out[name]["variable"] = safe_variable(name)

    return querystring_out


def get_parameters(parameters):
    """Get parameters from a function definition"""
    params_out = {}

    for parameter in parameters:

        param_out = {}
        # TODO
        # Resolve meta refs
        # if "$ref" in param.keys():
        #     meta_path = param["$ref"].split("/")
        #     del meta_path[0]
        #     print(meta_path)
        #     val = definition
        #     for nested_key in meta_path:
        #         val = val[nested_key]
        #     print(val)
        #     param = val
        #     # continue

        if "description" not in parameter.keys():
            logging.warning("No description for %s", parameter["name"])
            param_out["description"] = ""
            continue

        param_out["description"] = parameter["description"]
        name = safe_variable(parameter["name"])

        if "required" in parameter.keys():
            # If not required then add the default of None
            if not parameter["required"]:
                param_out["defaultValue"] = "None"

        if "type" in parameter.keys():
            param_out["type"] = normalise_type(parameter["type"])

        params_out[name] = param_out

    return params_out


# def find_parameter_refs(definition):
#     """Resolve internal parameter links"""
#     params_out = {}

#     for param in definition["parameters"]:
#         if "$ref" in definition["parameters"][param].keys():
#             ref_path = definition["parameters"][param]["$ref"].split("/")
#             del ref_path[0]
#             logging.info("Found internal reference %s", ref_path)
#             val = definition
#             for recursive_key in ref_path:
#                 val = val[recursive_key]
#             print(val)
#             param = val
#         params_out[ref_path(definition["parameters"][param]["name"].lower())] = param

#     return params_out
