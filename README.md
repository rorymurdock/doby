# Doby

[![Doby unit tests](https://github.com/rorymurdock/doby/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/rorymurdock/doby/actions/workflows/test.yml)
[![Coverage Status](https://coveralls.io/repos/github/rorymurdock/doby/badge.svg?branch=main)](https://coveralls.io/github/rorymurdock/doby?branch=main)

Named after [Doby](https://youtu.be/qX1Onl-n4NA?t=55) 🦈 from Anchorman 2

>You talk all that smack and that's the best name you come up with?

![](assets/doby.jpeg)

This library can be used to build REST API Libraries from either an open api spec json file via a generator or from a hand crafted json file. It will create the library with a `README.md` and `requirements.txt`. You can also create a `setup.py` and more, [see the advanced section](#advanced-usage) for more details

## Usage

### Building config

Use the generator library to download your open api spec file and make a config file. You will likely need to create a manual override file to go with it.

See any of the example generators in the `generator` folder.

### Making a library from config

You can run the make file directly and it will accept the positional arguments:

|Name|Value|Description|Optional|
|-|-|-|-|
|config|File path|The path to the config file to build|
|output directory|Folder path|The path where the library will be exported to|

And the optional argument of

|Name|Value|Description|Optional|
|-|-|-|-|
|-v||Enables debug logging|Yes|

Example:

`python3 -m doby "configs/api.json" "exports"`

## Doby JSON file structure

## Basic fields

These basic fields will configure the library
|Name|Description|Type|Optional|Sub key|value|type
|-|-|-|-|-|-|-|
|name|Name of the library & class with no spaces|`str`|||||
|description|Description of the library|`str`|||||
|debug|Enables debug logging|`bool`|yes||||
|requirements|A list of python requirements. you can view a list of automatically added [here](doby/build/imports.py#L14) in `import_list`|`dict`|yes||||
|||||name|name of the requirement|`str`|
||||yes|operator|Used in the requirements.txt file {`==`, `>=`, `~=`}|`str`|
||||yes|version|version you want for the above|`str`|
||||yes|builtin|Is this a built-in package? If so it won't be added to the `requirements.txt`|`bool`|
|hostname|The base hostname for the library, you'd be best to load this from a function using the function sub key|`dict`|||||
|||||`static`|Static value for the hostname|`str`|||||
|||||`variable`|Variable that has the hostname assigned|`str`|||||
|||||`function`|Function that returns the hostname|`str`|||||
|headers|A HTTP inferace is created for each header, you can create an empty header if you wish. For more information see the [header section](#headers)|`dict`|||||

Config Example

```json
{
    "name": "fruitStand",
    "description": "fruitStand configuration library",
    "debug": true,
    "requirements": {
        "os": {
            "builtin": true
        }
    },
    "hostname": {
        "function": "get_url()"
    },
    "headers": {
        "rest": {
            "Accept": {
                "static": "application/json"
            }
        }
    }
}
```

### Headers

The headers are set via a name dict in the format of

|Name|Description|Type|Optional|Sub key|value|type
|-|-|-|-|-|-|-|
|{header name}|Name of the library & class with no spaces|`dict`|||||
|||||{header key|Name of the key to send|`dict`|||||

### Dynamically generated keys

|Name|Description|Type|Optional|Sub key|value|type
|-|-|-|-|-|-|-|
|{header key}|Name of the key to send|`dict`|||||
|||||`static`|Static value for the header key value|`str`|
|||||`variable`|Variable that has the header key value assigned|`str`|
|||||`function`|Function that returns the header key value|`str`|

Config Example

```json
{
    "headers": {
        "rest": {
            "Accept": {
                "static": "application/json"
            },
            "version": {
                "variable": "api_version"
            },
            "api-key": {
                "function": "get_api_key()"
            }
        }
    }
}
```

## Functions

There are four kinds of functions you can create.

* init
* main
* endpoint
* custom

Endpoint is an function that will query the API and the code is automatically generated.

Custom is a function that you need to specify the code in a list of lines.

### Init code

Used to inject code into the class ___init__()_ function. Useful for getting config.

|Name|Description|Type|Optional|Sub key|value|type
|-|-|-|-|-|-|-|
|description|Description of what the function does|`dict`|||||
|parameters|Parameters you want to be used. For more information see the [parameters section](#parameters)|`dict`|||||
|code|A list of lines of code you want to add|`list`|||||

```json
{
    "init": {
        "description": "This is called when the class is initialised",
        "parameters": {
            "debug": {
                "description": "Enables debugging",
                "type": "bool",
                "defaultValue": "False"
            }
        },
        "code": [
            "print('hello')"
        ]
    }
}
```

### Main code

Adds a main function to the library if you want to launch it directly

|Name|Description|Type|Optional|Sub key|value|type
|-|-|-|-|-|-|-|
|description|Description of what the function does|`dict`|||||
|run|If `True` then a `if __name__ == "__main__"` statement is added and main is run|`dict`|Yes||||
|code|A list of lines of code you want to add|`list`|||||

```json
{
    "main": {
        "run": true,
        "description": "This is the main function",
        "code": [
            "fruit = fruitStand()",
            "print(fruit.getStock('Apples'))"
        ]
    }
}
```

### Endpoint

|Name|Description|Type|Optional|Sub key|value|type
|-|-|-|-|-|-|-|
|{function_name}|Name of the function definition|`dict`|||||

|Name|Description|Type|Optional|Sub key|value|type
|-|-|-|-|-|-|-|
|name|Function name|`str`|||||
|description|Description of what the function does|`dict`|||||
|method|What method to use eg. get, post, put|`str`|||||
|path|The URL path to the endpoint `/api/getStock`|`str`|||||
|header|The name of the header you want to use|`str`|||||
|returns|What you want to return|`str`|yes||||
|checkHttpResponse|Check the response against a [list of acceptable HTTP response codes](doby/build/) and returns a `json` object|`bool`|yes||||
|expectedHttpCode|Works in combination with `checkHttpResponse` to check if an expected code was returned|`int`|yes||||
|payload|The payload for the http request|`dict`|yes||||
|||||{payload_key_name}|[Dynamically generated key](#dynamically-generated-keys)|`dict`|||||
|querystring|The querystring for the http request|`dict`|yes||||
|||||{querystring_key_name}|[Dynamically generated key](#dynamically-generated-keys)|`dict`|||||
|parameters|Parameters you want to be used. For more information see the [parameters section](#parameters)|`dict`|yes||||
|code|A list of lines of code you want to add|`dict`|yes||||
|||||start|A list of lines of code to insert at the of the start function before anything else|`list`|||||
|||||mid|A list of lines of code to insert after the querystring and payload of the function but before the http request|`list`|||||
|||||end|A list of lines of code to insert at the end of the function after the http request but before the return|`list`|||||

This configures the functions that are created in the library

### Custom functions

Functions that are added to the library at the end, these could be functions for getting authentication details or modifying arguments.

|Name|Description|Type|Optional|Sub key|value|type
|-|-|-|-|-|-|-|
|{function_name}|Name of the function definition|`dict`|||||

|Name|Description|Type|Optional|Sub key|value|type
|-|-|-|-|-|-|-|
|name|Function name|`str`|||||
|description|Description of what the function does|`dict`|||||
|parameters|Parameters you want to be used. For more information see the [parameters section](#parameters)|`dict`|||||
|code|A list of lines of code you want to add|`list`|||||

```json
{
    "custom": {
        "get_api_key": {
            "name": "get_api_key",
            "description": "Custom test description",
            "parameters": {
                "self": {
                    "description": "Class built-in"
                }
            },
            "code": [
                "return self.auth['api-key']"
            ]
        }
    }
}
```

### Parameters

The Parameters are set via a name dict in the format of

|Name|Description|Type|Optional|Sub key|value|type
|-|-|-|-|-|-|-|
|{parameter name}|Name of the parameter|`dict`|||||
|||||Description|What the parameter does|`str`|||||
||||Yes|type|What type should the function expect|`str`|||||
||||Yes|defaultValue|A default value for the parameter|`str`|||||

Config Example

```json
{
    "parameters": {
        "debug": {
            "description": "Enables debugging",
            "type": "bool",
            "defaultValue": "False"
        }
    }
}
```

## Overriding auto generated files

When you have your base json file you can also add an override json file. As there's no URL auto generated, let's add one in. And say for example the API endpoint is named `sharks` but you want to name it `getSharks` and have a different description. Create an override json file as such:

`{filename}_override.py`

```json
{
    "url": "api.sharks.net",
    "functions": {
        "sharks": {
            "name": "getSharks",
            "description": "This will get an array of all sharks nearby"
        }
    }
}
```

When doby runs (swims?) it will merge the two files with the override taking priority.

## Advanced usage

### Setup.py

If you want to build this into a full packge you can enable a `setup.py` to be generated by specifying the below in a `setup.py` key

|Name|Description|Type|Optional|Sub key|value|type
|-|-|-|-|-|-|-|
|version|Package version|`str`|||||
|author|Who made this package|`str`|||||
|author_email|Email address for author|`str`|||||
|url|URL for the package info|`str`|||||
|developmentStatus|A `Development Status::` [classifier](https://pypi.org/classifiers/)|`str`|yes||||
|license|A `License ::` [classifier](https://pypi.org/classifiers/)|`str`|yes||||
|operatingSystem|A `Operating System ::` [classifier](https://pypi.org/classifiers/)|`str`|yes||||
|pythonVersion|A `Programming Language ::` [classifier](https://pypi.org/classifiers/)|`str`|yes||||

This will output a `setup.py`

```json
{
    "version": "1.0.0"
}
```

### .gitignore

Specify a list of files to be ignored by git

|Name|Description|Type|Optional|Sub key|value|type
|-|-|-|-|-|-|-|
|.gitignore|A list of files / folders for git to ignore|`list`|yes||||

```json
{
    ".gitignore": [
        "*.pyc"
    ]
}
```
