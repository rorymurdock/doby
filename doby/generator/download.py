import json
import reqrest
import logging

def download_swagger_index_files(hostname, path):
    """Download swagger index"""
    print("Downloading swagger index")
    response = reqrest.REST(url=hostname).get(path)

    swagger_index = json.loads(response.text)

    for api in swagger_index["apis"]:
        download_swagger_file(hostname, api["url"], api["name"], api["api_uid"])

    print("Downloading completed")

def download_swagger_file(hostname, path, name, name_2=None):
    """Download the swagger file"""
    print("Downloading %s" % name)
    swagger_file = reqrest.REST(url=hostname).get(path)

    if swagger_file.status_code != 200:
        print("Error downloading %s" % hostname + path)
        return False

    return swagger_file.text
