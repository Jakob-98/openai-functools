# [openai-functools](https://github.com/Jakob-98/openai-functools)

`openai-functools` is a Python library designed to enhance the functionality of OpenAI's 1 `gpt-3.5-turbo-0613` and `gpt-4-0613` models for function calling. This library focuses on generating the required JSON automatically by wrapping existing Python functions in our decorator. This removes the need for you to manually create and manage the JSON structures required for function calling in these models.

## Installation

This package is hosted on PyPI and can be installed with pip:

```sh
pip install openai-functools
```

Alternatively, you can clone this repository and install with Poetry:

```sh
git clone https://github.com/Jakob-98/openai-functools.git
cd openai-functools
poetry install
```

## Usage

To use `openai-functools`, import the package and wrap your function with the provided decorator. First, a **naive example** which does not use our libary (see `./examples/naive_approach.py`):

```python
def get_current_weather(location, unit="fahrenheit"):
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)

def run_conversation():
    messages = [{"role": "user", "content": "What's the weather like in London?"}]
    functions = [
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        }
    ]

    ... # call openai,  call the function using the response, call the OpenAI model again, etc..
```

Instead, our **novel approach**, we automatically generate the neccesary function parameters, and the above now becomes:

```python
from openai_functools import openai_function

@openai_function
def get_current_weather(location, unit="fahrenheit"):
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)

def run_conversation():
    messages = [{"role": "user", "content": "What's the weather like in London?"}]
    functions = [
        get_current_weather.openai_metadata
    ]

```

### Using the orchestrator

**todo**

### Using docstrings to enhance metadata

By using docstrings in your functions, we are able to extract more information to fill in the descriptions of the function and its properties. This will automatically be added to the openai function metadata, and will help the model better understand the functions and parameters.

Currently, only "reStructuredText" (reST) is supported by default, although this can be extended in the future (feel free to contribute!). Under the hood we make use of [docstring parser](https://pypi.org/project/docstring-parser/) to enable this.

## Examples

**TODO** add proper example, current ones are from PoC project and outdated.

Several examples can be found in the `examples` directory of this repository. Each example provides a concrete implementation of how to use `openai-functools` in different scenarios.

## Contributing

We welcome contributions to `openai-functools`! Please see our [contributing guide](CONTRIBUTING.md) for more details.

## Support

For support with `openai-functools`, please open an issue on this GitHub repository. We will do our best to assist you.

## License

`openai-functools` is licensed under the MIT license. See the [LICENSE](LICENSE) file for details.
