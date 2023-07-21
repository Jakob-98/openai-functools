import json
from typing import Any

from .function_spec import FunctionSpec
from .metadata_generator import extract_function_metadata


class FunctionsOrchestrator:

    def __init__(self, functions=None):
        if functions is None:
            functions = []
        self._functions = functions
        self._function_specs = []
        self._function_specs = self._create_function_specs(self.functions) \
            if self.functions is not None else []

    @property
    def functions(self):
        return self._functions

    @functions.setter
    def functions(self, functions):
        self._functions = functions
        self._function_specs = self._create_function_specs(self.functions) \
            if self.functions is not None else []

    @property
    def function_specs(self):
        return self._function_specs

    @function_specs.setter
    def function_specs(self, function_specs):
        self._function_specs = function_specs

    def register(self, function):
        self.functions.append(function)
        self._function_specs.append(self._create_function_spec(function))

    def register_all(self, functions):
        self.functions.extend(functions)
        self.function_specs.extend(self._create_function_specs(functions))

    def function(self, function):

        if function:
            self.functions.append(function)
            self.function_specs.append(self._create_function_spec(function))
            return function
        else:
            def wrapper(f):
                self.functions.append(f)
                self.function_specs.append(self._create_function_spec(f))
                return f

            return wrapper

    def call_functions(self, openai_response) -> Any:
        response_message = openai_response["choices"][0]["message"]
        responses = {}

        if response_message.get("function_call"):
            function_name = response_message["function_call"]["name"]
            function_args = json.loads(
                response_message["function_call"]["arguments"]
            )

            function = self._get_matching_function(function_name)

            if function is None:
                raise ValueError(
                    f'Function "{function_name}" is not '
                    f'registered with the orchestrator.'
                )

            responses[function_name] = function(**function_args)

        return responses

    def _get_matching_function(self, function_name):
        for spec in self.function_specs:
            if spec.name == function_name:
                return spec.func_ref

        return None

    def _create_function_specs(self, functions):
        return [self._create_function_spec(function) for function in functions]

    @staticmethod
    def _create_function_spec(function):
        return FunctionSpec(
            func_ref=function,
            parameters=extract_function_metadata(function)
        )

    @property
    def function_descriptions(self):
        return [spec.parameters for spec in self._function_specs]

    def create_function_descriptions(self, selected_functions=None):
        specs = self._function_specs

        if selected_functions is not None:
            specs = [spec for spec in specs if spec.name in selected_functions]

        return [spec.parameters for spec in specs]
