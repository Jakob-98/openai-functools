# OpenAI-Functools Example: Debugging Assistance

This is an example use-case of OpenAI-Functools, which provides a framework for orchestrating and automatically generating metadata for OpenAI functions.

## Example Use-Case: Debugging Assistance for Software Developers

In this use-case, we create an AI assistant that helps software developers streamline the debugging process of their applications. The assistant communicates the functionalities and aids users in understanding complex system structures. It's equipped with capabilities to fetch and interpret logs, interact with databases, connect with APIs, and even query vector databases for document retrieval. The aim is to provide real-time, insightful information that supports problem-solving and makes the debugging process faster and more efficient.

## How it works

1. The assistant is initialized with a system message that describes its functionalities.
2. A `FunctionsOrchestrator` object is created. This orchestrator will handle calling the appropriate functions based on the user's requests and the assistant's responses.
3. Four functions are defined and registered with the orchestrator. These functions provide the assistant's capabilities:
    - `retrieve_logs_by_date_and_vm_id`: retrieves logs from a specific date and a specific VM.
    - `retrieve_log_analytics_information`: retrieves aggregate log analytics information.
    - `retrieve_api_information`: queries an API based on the provided endpoint and parameters.
    - `query_vector_db`: queries a vector database with an embedded string and returns a piece of text based on similarity.
4. Helper functions `call_openai` and `handle_response` are used to handle the interaction with the OpenAI API and process its responses.
5. User interacts with the assistant by adding messages to the conversation, which the orchestrator then uses to decide which function to call.

In a debugging session, a user might ask the assistant to retrieve logs for a specific date, or to check the health of a particular VM. The assistant will call the appropriate function, return the result, and interpret it for the user, potentially recommending further actions based on the result.

## Requirements

You will need the following to run this example:

- Python 3.7 or later
- OpenAI Python v0.27.0
- OpenAI API key
- `openai_functools` package

To install the required package, use pip:

```bash
pip install openai-functools
```

## Running the example

Ensure that the OpenAI API key is set in your environment variables. If not, you can set it as follows:

```bash
export OPENAI_API_KEY='your-api-key'
```

Then, you can run this example in a Python environment or a Jupyter notebook.

## Customization

You can customize this example by defining your own functions and registering them with the orchestrator. These functions can interact with different services, databases, or APIs based on your needs. You can also adjust the `call_openai` and `handle_response` helper functions to suit your use-case.

Remember, this is a simplified example. In a real-world scenario, you would replace the spoof functions with real implementations. For instance, `generate_spoof_logs` could be replaced with a function that interacts with a real log management system. OpenAI-Functools Example: Debugging Assistance

This is an example use-case of OpenAI-Functools, which provides a framework for orchestrating and automatically generating metadata for OpenAI functions.
