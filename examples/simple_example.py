import json
import os
import openai
from openai_functools import openai_function, FunctionSpec


@openai_function
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
        functions=function_specs,
        function_call="auto",
    )
    response_message = response["choices"][0]["message"]
    print(f"response message: {response_message}")
