import json
import os
import openai
from openai_functools import function_metadata_decorator, FunctionSpec


@function_metadata_decorator
def get_current_weather(location, unit="fahrenheit"):
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)


if __name__ == "__main__":
    openai.api_key = os.environ["OPENAI_API_KEY"]
    openai_model = os.environ["OPENAI_MODEL"]
    messages = [{"role": "user", "content": "What's the weather like in Amsterdam?"}]
    function_specs = [
        FunctionSpec(
            func_ref=get_current_weather,
            parameters=get_current_weather.metadata
        )
    ]

    response = openai.ChatCompletion.create(
        model=openai_model,
        messages=messages,
        functions=functions,
        function_call="auto",
    )
    messages = [
        {"role": "user", "content": "What's the weather like in New York?"}
    ]

    response = openai_service.call_function(messages)
    print(response)