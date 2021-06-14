"""Generate WSO config from API spec"""
import logging
import json
from doby.generator import download, normalise, parameters, utils

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s\t%(funcName)s\t%(message)s")


def main(aw_host):
    """Make the config"""

    endpoint_allow_list = [
        "/info",
        "/devices/search",
        "/devices",
        "/operations/{operation-uuid}",
    ]
    config = {}
    config["functions"] = {}
    config["functions"]["endpoint"] = {}

    swagger_index = download.swagger_index_files(aw_host,
                                                 "/api/system/help/localjson")

    for api in swagger_index:
        file = download.swagger_file(aw_host, api["url"], api["name"])
        api_doc = json.loads(file)

        # TODO Fix the querystring "-" removal

        for path in api_doc["paths"]:
            logging.info("Reading path: %s", path)

            if path in endpoint_allow_list:
                # if True:
                for method in api_doc["paths"][path]:
                    logging.info("Reading path: %s method: %s", path, method)

                    spec = api_doc["paths"][path][method]
                    name = f"{method.lower()}{normalise.path(path)}v{normalise.version(spec['produces'])}"
                    logging.info("Building function %s()", name)

                    config["functions"]["endpoint"][name] = {}
                    func = config["functions"]["endpoint"][name]

                    func["name"] = name
                    func["description"] = utils.get_description(spec)
                    func["method"] = method.lower()
                    func[
                        "path"] = f"{api_doc['basePath']}{normalise.dynamic_path(path)}"
                    func["header"] = f"v{normalise.version(spec['produces'])}"
                    func["checkHttpResponse"] = True
                    func["filterQuerystring"] = True

                    querystring = parameters.querystring(spec["parameters"])
                    if querystring != {}:
                        func["querystring"] = querystring

                    params = parameters.get_parameters(spec["parameters"])
                    if params != {}:
                        func["parameters"] = params

    config_out = open("wso.json", "w")
    config_out.write(json.dumps(config, indent=4))
    config_out.close()


if __name__ == "__main__":
    main("as135.awmdm.com")
