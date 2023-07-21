# openai-functools

`openai-functools` is a Python library designed to enhance the functionality of OpenAI's gpt-3.5-turbo-0613 and gpt-4-0613 models for function calling. This library focuses on generating the required JSON automatically by wrapping existing Python functions in our decorator. This removes the need for you to manually create and manage the JSON structures required for function calling in these models.

## Installation

This package is hosted on PyPI and can be installed with pip:

```sh
pip install openai-functools
```

Alternatively, you can clone this repository and install with Poetry:

```sh
git clone https://github.com/username/openai-functools.git
cd openai-functools
poetry install
```

## Usage

To use `openai-functools`, import the package and wrap your function with the provided decorator:

```python
from openai_functools import openai_function

@openai_function
def my_function(arg1: str, arg2: int) -> str:
    # Your code here
```

This will automatically generate the necessary JSON structure for use with the Chat Completions API.

## Examples

Several examples can be found in the `examples` directory of this repository. Each example provides a concrete implementation of how to use `openai-functools` in different scenarios.

## Contributing

We welcome contributions to `openai-functools`! Please see our [contributing guide](CONTRIBUTING.md) for more details.

## Support

For support with `openai-functools`, please open an issue on this GitHub repository. We will do our best to assist you.

## License

`openai-functools` is licensed under the MIT license. See the [LICENSE](LICENSE) file for details.
