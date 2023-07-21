from openai_functools import FunctionsOrchestrator


def test_orchestrator_initialization_with_standard_functions():
    def function_one():
        return "function_one"

    def function_two():
        return "function_two"

    orchestrator = FunctionsOrchestrator(
        functions=[function_one, function_two]
    )
    assert orchestrator.functions == [function_one, function_two]
    assert orchestrator.function_specs != []


def test_orchestrator_initialization_with_decorated_functions():
    orchestrator = FunctionsOrchestrator()

    @orchestrator.function
    def function_one():
        return "function_one"

    @orchestrator.function
    def function_two():
        return "function_two"

    assert orchestrator.functions == [function_one, function_two]
    assert orchestrator.function_specs != []


def test_orchestrator_initialization_with_registration_methods():
    def function_one():
        return "function_one"

    def function_two():
        return "function_two"

    orchestrator = FunctionsOrchestrator()
    orchestrator.register_all([function_one, function_two])
    assert orchestrator.functions == [function_one, function_two]
    assert orchestrator.function_specs != []

    orchestrator = FunctionsOrchestrator()
    orchestrator.register(function_one)
    assert orchestrator.functions == [function_one]
    assert orchestrator.function_specs != []


def test_orchestrator_function_descriptions(
        expected_metadata, weather_function
):
    orchestrator = FunctionsOrchestrator(functions=[weather_function])
    assert orchestrator.function_descriptions != []
    assert orchestrator.create_function_descriptions() != []
    assert orchestrator.create_function_descriptions() \
           == orchestrator.function_descriptions
    assert orchestrator.function_descriptions == [expected_metadata]


def test_orchestrator_call_functions(weather_chat_response, weather_function):
    orchestrator = FunctionsOrchestrator(functions=[weather_function])
    results = orchestrator.call_functions(weather_chat_response)
    assert results == \
            {
               "get_current_weather":
                    '{"location": "Boston", '
                    '"temperature": "72", '
                    '"unit": "fahrenheit", '
                    '"forecast": ["sunny", "windy"]}'
            }
