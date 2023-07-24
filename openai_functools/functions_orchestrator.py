import json
from typing import Any, Callable, List, Optional, Dict

from openai_functools.function_spec import FunctionSpec
from openai_functools.metadata_generator import extract_openai_function_metadata

class FunctionsOrchestrator:
    def __init__(self, functions: Optional[List[Callable]] = None) -> None:
        self._functions = functions if functions is not None else []
        self._function_specs = self._create_function_specs(self._functions)

    @property
    def functions(self) -> List[Callable]:
        return self._functions

    @functions.setter
    def functions(self, functions: List[Callable]) -> None:
        self._functions = functions
        self._function_specs = self._create_function_specs(self._functions)

    @property
    def function_specs(self) -> List[FunctionSpec]:
        return self._function_specs

    def register(self, function: Callable) -> None:
        self._functions.append(function)
        self._function_specs.append(self._create_function_spec(function))

    def register_all(self, functions: List[Callable]) -> None:
        self._functions.extend(functions)
        self._function_specs.extend(self._create_function_specs(functions))

    def function(self, func: Optional[Callable] = None):
        if func is not None:
            self.register(func)
            return func

        def wrapper(f):
            self.register(f)
            return f

        return wrapper

    def call_functions(self, openai_response: dict) -> dict:
        response_message = openai_response["choices"][0]["message"]
        responses = {}

        if function_call := response_message.get("function_call"):
            function_name = function_call["name"]
            function_args = json.loads(function_call["arguments"])

            function = self._get_matching_function(function_name)

            if function is None:
                raise ValueError(
                    f'Function "{function_name}" is not '
                    f"registered with the orchestrator."
                )

            responses[function_name] = function(**function_args)

        return responses

    def _get_matching_function(self, function_name: str) -> Optional[Callable]:
        for spec in self._function_specs:
            if spec.name == function_name:
                return spec.func_ref
        return None

    def _create_function_specs(self, functions: List[Callable]) -> List[FunctionSpec]:
        return [self._create_function_spec(function) for function in functions]

    @staticmethod
    def _create_function_spec(function: Callable) -> FunctionSpec:
        return FunctionSpec(
            func_ref=function, parameters=extract_openai_function_metadata(function)
        )

    @property
    def function_descriptions(self) -> List[Dict[str, Any]]:
        return [spec.parameters for spec in self._function_specs]

    def create_function_descriptions(self, selected_functions: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        specs = self._function_specs if selected_functions is None else [spec for spec in self._function_specs if spec.name in selected_functions]
        return [spec.parameters for spec in specs]

