from pytest import fixture
import json

@fixture
def weather_function():
    def get_current_weather(location, unit="fahrenheit"):
        weather_info = {
            "location": location,
            "temperature": "72",
            "unit": unit,
            "forecast": ["sunny", "windy"],
        }
        return json.dumps(weather_info)

    return get_current_weather


@fixture()
def expected_metadata():
    return {
        "name": "get_current_weather",
        "description": "get_current_weather",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "location"},
                "unit": {
                    "type": "string",
                    "description": "unit",
                    "default": "fahrenheit",
                },
            },
            "required": ["location"],
        },
    }


@fixture()
def weather_chat_response():
    return {
        "id": "chatcmpl-7elUo0WOn1SxvYJPEx3TOprJMJeac",
        "object": "chat.completion",
        "created": 1689950050,
        "model": "gpt-3.5-turbo-0613",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "null",
                    "function_call": {
                        "name": "get_current_weather",
                        "arguments": "{\n  \"location\": \"Boston\"\n}"
                    }
                },
                "finish_reason": "function_call"
            }
        ],
        "usage": {
            "prompt_tokens": 68,
            "completion_tokens": 16,
            "total_tokens": 84
        }
    }
