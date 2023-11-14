# Import the langchain library
import langchain

from openai_functools import FunctionsOrchestrator
from openai_functools.metadata_generator import openai_function


@openai_function
def transform_text(text: str) -> str:
    # Use the langchain library to transform the text
    transformed_text = langchain.transform(text)
    return transformed_text


# Instantiate a FunctionsOrchestrator
orchestrator = FunctionsOrchestrator()

# Register the transform_text function with the orchestrator
orchestrator.register(transform_text)

# Create a dictionary that represents an OpenAI response
openai_response = {
    "choices": [
        {
            "message": {
                "function_call": {
                    "name": "transform_text",
                    "arguments": '{"text": "Hello, world!"}',
                }
            }
        }
    ]
}

# Use the orchestrator to call the function specified in the OpenAI response
result = orchestrator.call_function(openai_response)

# Print the result of the function call
print(result)
