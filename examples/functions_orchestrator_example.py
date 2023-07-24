import json

import openai

from openai_functools import FunctionsOrchestrator


def get_current_weather(location, unit="fahrenheit"):
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)


orchestrator = FunctionsOrchestrator()
orchestrator.register(get_current_weather)

openai.api_key = "sk-<>"
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=[{"role": "user", "content": "What's the weather like in Boston?"}],
    functions=orchestrator.create_function_descriptions(),
    function_call="auto",
)


if __name__ == "__main__":
    function_results = orchestrator.call_functions(response)
    print(function_results)
