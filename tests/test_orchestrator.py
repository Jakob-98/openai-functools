import pytest

from openai_functools import FunctionsOrchestrator

def test_orchestrator_initialization_with_decorated_function():
    orchestrator = FunctionsOrchestrator()

    @orchestrator.function
    def function_one():
        return "function_one"

    @orchestrator.function
    def function_two():
        return "function_two"

    assert function_one.__name__ in orchestrator._functions.keys()
    assert function_two.__name__ in orchestrator._functions.keys()

def test_orchestrator_initialization_with_standard_function():
    orchestrator = FunctionsOrchestrator()

    def function_one():
        return "function_one"

    def function_two():
        return "function_two"

    orchestrator.register_all([function_one, function_two])
    assert function_two.__name__ in orchestrator._functions.keys()
    assert function_one.__name__ in orchestrator._functions.keys()


def test_orchestrator_function_descriptions(expected_metadata, weather_function):
    orchestrator = FunctionsOrchestrator(functions=[weather_function])
    assert orchestrator.function_descriptions != []
    assert orchestrator.create_function_descriptions() != []
    assert (
        orchestrator.create_function_descriptions()
        == orchestrator.function_descriptions
    )
    assert orchestrator.function_descriptions == [expected_metadata]


def test_orchestrator_call_functions(weather_chat_response, weather_function):
    orchestrator = FunctionsOrchestrator(functions=[weather_function])
    results = orchestrator.call_function(weather_chat_response)
    assert (
        results
        == '{"location": "Boston", "temperature": "72", "unit": "fahrenheit", "forecast": ["sunny", "windy"]}'
    )


def test_call_unregistered_function_raises_error():
    orchestrator = FunctionsOrchestrator()

    with pytest.raises(KeyError):
        orchestrator.call_function(
            {
                "choices": [
                    {
                        "message": {
                            "function_call": {
                                "name": "unregistered_function",
                                "arguments": "{}",
                            }
                        }
                    }
                ]
            }
        )


def test_register_non_callable_raises_error():
    orchestrator = FunctionsOrchestrator()

    with pytest.raises(TypeError):
        orchestrator.register("not_a_function")


def test_register_duplicate_function():
    orchestrator = FunctionsOrchestrator()

    def function_one():
        return "function_one"

    orchestrator.register(function_one)

    with pytest.raises(ValueError):
        orchestrator.register(function_one)

    with pytest.raises(ValueError):
        orchestrator.register_all([function_one])

    with pytest.raises(ValueError):
        orchestrator.functions = [function_one, function_one]
