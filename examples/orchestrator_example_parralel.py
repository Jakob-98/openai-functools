import json
import os

import openai

from openai_functools import FunctionsOrchestrator

import openai
import json

def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    if "Tokyo" in location.lower():
        return json.dumps({"location": location, "temperature": "10", "unit": "celsius"})
    elif "San Francisco" in location.lower():
        return json.dumps({"location": location, "temperature": "72", "unit": "fahrenheit"})
    else:
        return json.dumps({"location": location, "temperature": "22", "unit": "celsius"})


orchestrator = FunctionsOrchestrator()
orchestrator.register_all([get_current_weather])


if __name__ == "__main__": #FIXME: it currently only returns 1 location, why?
    openai.api_key = os.environ["OPENAI_API_KEY"]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[{"role": "user", "content": "What's the weather like in Toyko, Boston, and San Fransisco?"}],
        tools=[{"type": "function", #FIXME: we want to generate a list of these tools automatically
               "function": orchestrator.create_function_descriptions()[0]
               }],
        tool_choice="auto",
    )
    # Call the function that is specified in the response
    print(orchestrator.call_function(response))

