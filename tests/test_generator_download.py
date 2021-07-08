"""Doby generator download testing"""
import json
from unittest import mock
from doby.generator import download
from . import get_random


# @mock.patch("doby.generator.reqrest")
# @mock.patch("doby.generator.request.Response")
@mock.patch("doby.generator.download.reqrest.REST.get")
def test_swagger_index_files(mock_response):
    """Test swagger_index_files"""

    mock_value = get_random.text()

    mock_response_text = {}
    mock_response_text["apis"] = mock_value
    mock_response.return_value.status_code = 200
    mock_response.return_value.text = json.dumps(mock_response_text)

    test = download.swagger_index_files("mock.swagger.io", "/v1/swagger.json")

    assert test == mock_value


@mock.patch("doby.generator.download.reqrest.REST.get")
def test_swagger_file(mock_response):
    """Test swagger_file"""

    mock_value = get_random.text()
    mock_key = get_random.text()

    mock_response_text = {}
    mock_response_text[mock_key] = mock_value
    mock_response.return_value.status_code = 200
    mock_response.return_value.text = json.dumps(mock_response_text)

    test = download.swagger_file("mock.swagger.io", "/v1/swagger.json", "")

    assert test == json.dumps(mock_response_text)


@mock.patch("doby.generator.download.reqrest.REST.get")
def test_swagger_file_bad_response(mock_response):
    """Test swagger_file"""

    mock_response.return_value.status_code = 201

    test = download.swagger_file("mock.swagger.io", "/v1/swagger.json", "")

    assert test is False
