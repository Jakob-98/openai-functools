# Examples

This folder contains examples of how to use the library.
The examples are organized by the type of use case they demonstrate.

- [Naive approach](./1_naive_approach.ipynb)
- [Simple example based on the naive approach](./simple_example.py)
- [Simple Example with two functions and calling them with the orchestrator](./example_with_two_functions.py)

- [Example with Langchain](./langchain_example.py)
## Example with Langchain

This example demonstrates how to integrate the `openai-functools` library with the `langchain` library. The `langchain` library is used to transform text, and this transformation function is registered with the `FunctionsOrchestrator` from the `openai-functools` library. The orchestrator is then used to call the transformation function based on an OpenAI response.

To run this example, navigate to the `examples` directory and run the following command:

```bash
python langchain_example.py
```

Please note that you need to have the `langchain` library installed in your environment to run this example. You can install it using pip:

```bash
pip install langchain
```
