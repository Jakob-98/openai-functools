import json
import logging
from typing import Any, Callable, Dict, List, Optional

from openai_functools.function_spec import FunctionSpec
from openai_functools.metadata_generator import \
    extract_openai_function_metadata


class FunctionsOrchestrator:
    def __init__(self, functions: Optional[List[Callable]] = None) -> None:
        logging.info("Called FunctionsOrchestrator.__init__")
        self._functions = []
        self._function_specs = []

        if functions is not None:
            for function in functions:
                self._add_function(function)

    @property
    def functions(self) -> List[Callable]:
        return self._functions

    @functions.setter
    def functions(self, functions: List[Callable]) -> None:
        for function in functions:
            self._add_function(function)

    @property
    def function_specs(self) -> List[FunctionSpec]:
        return self._function_specs

    def register(self, function: Callable) -> None:
        logging.info(f"Called register with function {function.__name__}")
        self._add_function(function)
        logging.info(f"Completed register with function {function.__name__}")

    def register_all(self, functions: List[Callable]) -> None:

        for function in functions:
            self._add_function(function)

    def _add_function(self, function: Callable) -> None:
        logging.info(f"Called _add_function with function {function.__name__}")

        if not callable(function):
            logging.error(f'Function "{function}" is not callable.')
            raise TypeError(
                f'Function "{function}" is not callable.'
            )

        if self._functions is None:
            self._functions = []
            self._function_specs = []

        matching_function = self._get_matching_function(function.__name__)

        if matching_function is not None:
            raise ValueError(
                f'Function "{function.__name__}" is already registered.'
            )

        logging.info(f"Adding function {function.__name__} to _functions and _function_specs")
        self._functions.append(function)
        self._function_specs.append(self._create_function_spec(function))
        logging.info(f"Completed _add_function with function {function.__name__}")

    def function(self, func: Optional[Callable] = None):
        if func is not None:
            self.register(func)
            return func

        def wrapper(f):
            self.register(f)
            return f

        return wrapper

    def call_function(self, openai_response: dict) -> dict:
        response_message = openai_response["choices"][0]["message"]
        responses = {}

        if function_call := response_message.get("function_call"):
            function_name = function_call["name"]
            function_args = json.loads(function_call["arguments"])
            function = self._get_matching_function(function_name)

            if function is None:
                logging.error(f'Function "{function_name}" is not registered with the orchestrator.')
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
        logging.info(f"Called _create_function_spec with function {function.__name__}")
        spec = FunctionSpec(
            func_ref=function, parameters=extract_openai_function_metadata(function)
        )
        logging.info(f"Completed _create_function_spec with function {function.__name__}")
        return spec

    @property
    def function_descriptions(self) -> List[Dict[str, Any]]:
        return [spec.parameters for spec in self._function_specs]

    def create_function_descriptions(
        self, selected_functions: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        specs = (
            self._function_specs
            if selected_functions is None
            else [
                spec for spec in self._function_specs if spec.name in selected_functions
            ]
        )
        return [spec.parameters for spec in specs]
