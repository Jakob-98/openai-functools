import os
import json
import openai
from openai_functools import FunctionsOrchestrator


def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
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
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)


orchestrator = FunctionsOrchestrator()
orchestrator.register_all([get_current_weather, get_weather_next_day])


if __name__ == "__main__":
    openai.api_key = os.environ["OPENAI_API_KEY"]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            {"role": "user", "content": "What's the weather like in Boston?"}],
        functions=orchestrator.create_function_descriptions(),
        function_call="auto",
    )
    # Call the function that is specified in the response
    print(orchestrator.call_function(response))

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            {"role": "user", "content": "What's the weather like in Boston tomorrow?"}],
        functions=orchestrator.create_function_descriptions(),
        function_call="auto",
    )
    # Call the function that is specified in the response
    print(orchestrator.call_function(response))


