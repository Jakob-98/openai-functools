import json
import os

import openai

from openai_functools import FunctionsOrchestrator


def get_info_from_db():
    """
    Get information from a database

    The database contains information about: ...
    """

    return

def get_info_from_api():
    """
    Get information from an API

    The API contains information about: ...
    """

    return

def get_info_from_file():
    """
    Get information from a file

    The file contains information about: ...
    """

    return


"""

# Scenario: maintenance/logging/alert/debugging application/UI
# needs to read logs, fetch data from db, fetch data from api depending on the query

User: what is "XYZ" -> needs api 

User: what is "ABC" -> needs db

User: fetch the logs -> needs to read local logfile

Vector database for docs about "XYZ"

# scenario: in database, event is added that gives warning about "XYZ"
# user checks the database row to see what the warning is about
# user requests log from the application for day XYZ
# user checks endpoint for "XYZ" to see if it is still running
# user reads the documentation about "XYZ" asking vector database

"""


def system_prompt() -> str:
    """Generate a system prompt"""
    return "What's the weather like in Boston?"









# def get_current_weather(location, unit="fahrenheit"):
#     """Get the current weather in a given location"""
#     weather_info = {
#         "location": location,
#         "temperature": "72",
#         "unit": unit,
#         "forecast": ["sunny", "windy"],
#     }
#     return json.dumps(weather_info)


# def get_weather_next_day(location, unit="fahrenheit"):
#     """Get the weather forecast for the next day in a given location"""
#     weather_info = {
#         "location": location,
#         "temperature": "72",
#         "unit": unit,
#         "forecast": ["sunny", "windy"],
#     }
#     return json.dumps(weather_info)


# orchestrator = FunctionsOrchestrator()
# orchestrator.register_all([get_current_weather, get_weather_next_day])


# if __name__ == "__main__":
#     openai.api_key = os.environ["OPENAI_API_KEY"]
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo-0613",
#         messages=[{"role": "user", "content": "What's the weather like in Boston?"}],
#         functions=orchestrator.create_function_descriptions(),
#         function_call="auto",
#     )
#     # Call the function that is specified in the response
#     print(orchestrator.call_function(response))

#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo-0613",
#         messages=[
#             {"role": "user", "content": "What's the weather like in Boston tomorrow?"}
#         ],
#         functions=orchestrator.create_function_descriptions(),
#         function_call="auto",
#     )
#     # Call the function that is specified in the response
#     print(orchestrator.call_function(response))

