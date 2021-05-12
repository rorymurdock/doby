"""Doby README testing"""
from doby.build import setup_py


def test_build_setup_empty():
    """Test build_setup_empty"""

    function = {}

    assert setup_py.build_setup(function) == ""


def test_build_setup_one_required_key_missing():
    """Test build_setup_one_required_key_missing"""

    function = {}
    function["description"] = "fruitTest configuration library"
    function["name"] = "fruitTest"
    function["setup"] = {}
    function["requirements"] = {
        "apple": {},
        "orange": {"builtin": True, "operator": "==", "version": "1.0.0"},
        "pear": {"builtin": False, "operator": "==", "version": "1.0.0"},
        "lime": {"builtin": False, "operator": "=="},
    }
    setup = function["setup"]
    setup["author"] = "Me"
    setup["author_email"] = "me@example.com"
    setup["url"] = "https://example.com"

    assert setup_py.build_setup(function) == ""


def test_build_setup_no_extras():
    """Test build_setup_no_extras"""

    function = {}
    function["description"] = "fruitTest configuration library"
    function["name"] = "fruitTest"
    function["setup"] = {}
    function["requirements"] = {
        "apple": {},
        "orange": {"builtin": True, "operator": "==", "version": "1.0.0"},
        "pear": {"builtin": False, "operator": "==", "version": "1.0.0"},
        "lime": {"builtin": False, "operator": "=="},
    }
    setup = function["setup"]
    setup["version"] = "1.0.0"
    setup["author"] = "Me"
    setup["author_email"] = "me@example.com"
    setup["url"] = "https://example.com"

    assert setup_py.build_setup(function) == [
        "import setuptools",
        "",
        'with open("README.md", "r") as fh:',
        "    LONG_DESCRIPTION = fh.read()",
        "",
        'setuptools.setup(name="fruitTest", version="1.0.0", author="Me", '
        'author_email="me@example.com", url="https://example.com", '
        'description="fruitTest configuration library", '
        "long_description=LONG_DESCRIPTION, "
        'long_description_content_type="text/markdown", classifiers=[], '
        "install_requires=['reqrest', 'apple', 'pear', 'lime'], "
        "include_package_data=True)",
    ]


def test_build_setup_all():
    """Test build_setup_all"""

    function = {}
    function["description"] = "fruitTest configuration library"
    function["name"] = "fruitTest"
    function["setup"] = {}
    function["requirements"] = {
        "apple": {},
        "orange": {"builtin": True, "operator": "==", "version": "1.0.0"},
        "pear": {"builtin": False, "operator": "==", "version": "1.0.0"},
        "lime": {"builtin": False, "operator": "=="},
    }
    setup = function["setup"]
    setup["version"] = "1.0.0"
    setup["author"] = "Me"
    setup["author_email"] = "me@example.com"
    setup["url"] = "https://example.com"
    setup["developmentStatus"] = "5 - Production/Stable"
    setup["license"] = "OSI Approved :: Apache Software License"
    setup["operatingSystem"] = "OS Independent"
    setup["pythonVersion"] = "Python :: 3"

    assert setup_py.build_setup(function) == [
        "import setuptools",
        "",
        'with open("README.md", "r") as fh:',
        "    LONG_DESCRIPTION = fh.read()",
        "",
        'setuptools.setup(name="fruitTest", version="1.0.0", author="Me", '
        'author_email="me@example.com", url="https://example.com", '
        'description="fruitTest configuration library", '
        "long_description=LONG_DESCRIPTION, "
        'long_description_content_type="text/markdown", classifiers=["Development '
        'Status :: 5 - Production/Stable","License Status :: OSI Approved :: Apache '
        'Software License","Operating System :: OS Independent","Programming Language '
        ":: Python :: 3\",], install_requires=['reqrest', 'apple', 'pear', "
        "'lime'], include_package_data=True)",
    ]
