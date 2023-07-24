import json
import os

import openai

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
    openai.api_key = os.getenv("OPENAI_API_KEY")

    messages = [{"role": "user", "content": "What's the weather like in London?"}]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=[get_current_weather.openai_metadata],
        function_call="auto",
    )

    response_message = response["choices"][0]["message"]

    if response_message.get("function_call"):
        function_name = response_message["function_call"]["name"]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = get_current_weather(**function_args)

        messages.append(
            {"role": "function", "name": function_name, "content": function_response}
        )
        messages.append(response_message)

        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
        )
        return second_response


if __name__ == "__main__":
    print(run_conversation())
