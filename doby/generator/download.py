"""Doby config generator"""
import json
import logging
import reqrest


def swagger_index_files(hostname, path):
    """Download swagger index"""
    logging.info("Downloading swagger index")

    response = reqrest.REST(url=hostname).get(path)
    swagger_index = json.loads(response.text)

    return swagger_index["apis"]


def swagger_file(hostname, path, name):
    """Download the swagger file"""
    logging.info("Downloading %s", name)

    response = reqrest.REST(url=hostname).get(path)

    if response.status_code != 200:
        logging.error("Error downloading %s" % hostname + path)
        return False

    return response.text
