import json
import os

from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

from openai_functools import FunctionsOrchestrator


def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    if "Tokyo" in location.lower():
        return json.dumps(
            {"location": location, "temperature": "10", "unit": "celsius"}
        )
    elif "San Francisco" in location.lower():
        return json.dumps(
            {"location": location, "temperature": "72", "unit": "fahrenheit"}
        )
    else:
        return json.dumps(
            {"location": location, "temperature": "22", "unit": "celsius"}
        )


orchestrator = FunctionsOrchestrator()
orchestrator.register_all([get_current_weather])


if __name__ == "__main__":
    response = client.chat.completions.create(model="gpt-3.5-turbo-1106",
    messages=[
        {
            "role": "user",
            "content": "What's the weather like in Toyko, Boston, and San Fransisco?",
        }
    ],
    tools=orchestrator.create_tools_descriptions(),
    tool_choice="auto")
    # Call the function that is specified in the response
    print(orchestrator.call_function(response))
