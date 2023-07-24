# [openai-functools](https://github.com/Jakob-98/openai-functools)

`openai-functools` is a Python library designed to enhance the functionality of OpenAI's `gpt-3.5-turbo-0613` and `gpt-4-0613` models for function calling. This library focuses on generating the required JSON/dictionary/metadata automatically by wrapping existing Python functions in our decorator. This removes the need for you to manually create and manage the JSON structures required for function calling in these models.

## Why openai-functools

![example](./example.png)

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

Ensure your environment variable `OPENAI_API_KEY` is set.

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
import json
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

```python
from openai_functools import FunctionsOrchestrator

def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather forecast in a given location"""
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)

def get_weather_next_day(location, unit="fahrenheit"):
    """Get the weather forecast for the next day in a given location"""
    weather_info = {
        "location": location,
        "temperature": "78",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)

orchestrator = FunctionsOrchestrator()
orchestrator.register_all([get_current_weather, get_weather_next_day])
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=[{"role": "user", "content": "What's the weather like in Boston?"}],
    functions=orchestrator.create_function_descriptions(),
    function_call="auto",
)
function_results = orchestrator.call_function(response)
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=[{"role": "user", "content": "What's the weather like in Boston tomorrow?"}],
    functions=orchestrator.create_function_descriptions(),
    function_call="auto",
)
function_results = orchestrator.call_function(response)
```
### Using docstrings to enhance metadata

By using docstrings in your functions, we are able to extract more information to fill in the descriptions of the function and its properties. This will automatically be added to the openai function metadata, and will help the model better understand the functions and parameters.

Currently, only "reStructuredText" (reST) is supported by default, although this can be extended in the future (feel free to contribute!). Under the hood we make use of [docstring parser](https://pypi.org/project/docstring-parser/) to enable this.

## Examples

Several examples can be found in the `examples` directory of this repository.

## Contributing

We welcome contributions to `openai-functools`! Please see our [contributing guide](CONTRIBUTING.md) for more details.

## Support

For support with `openai-functools`, please open an issue on this GitHub repository. We will do our best to assist you.

## License

`openai-functools` is licensed under the MIT license. See the [LICENSE](LICENSE) file for details.
