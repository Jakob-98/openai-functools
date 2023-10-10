import json
import os

import openai

from openai_functools import FunctionsOrchestrator


class WeatherService:
    def __init__(self, location):
        self.location = location

    def get_current_weather(self, unit="fahrenheit"):
        """Get the current weather in a given location"""
        weather_info = {
            "location": self.location,
            "temperature": "72",
            "unit": unit,
            "forecast": ["sunny", "windy"],
        }
        return json.dumps(weather_info)

    def get_weather_next_day(self, unit="fahrenheit"):
        """Get the weather forecast for the next day in a given location"""
        weather_info = {
            "location": self.location,
            "temperature": "75",
            "unit": unit,
            "forecast": ["sunny", "windy"],
        }
        return json.dumps(weather_info)


weatherService = WeatherService("Boston")
orchestrator = FunctionsOrchestrator()
orchestrator.register_instance(weatherService)

# You can also register methods individually:
# orchestrator.register_all([weatherService.get_current_weather, weatherService.get_weather_next_day])

if __name__ == "__main__":
    openai.api_key = os.environ["OPENAI_API_KEY"]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[{"role": "user", "content": "What's the weather like in Boston?"}],
        functions=orchestrator.create_function_descriptions(),
        function_call="auto",
    )
    # Call the function that is specified in the response
    print(orchestrator.call_function(response))

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            {"role": "user", "content": "What's the weather like in Boston tomorrow?"}
        ],
        functions=orchestrator.create_function_descriptions(),
        function_call="auto",
    )
    # Call the function that is specified in the response
    print(orchestrator.call_function(response))
