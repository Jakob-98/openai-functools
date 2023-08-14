import json
from typing import Any, Callable, Dict, List, Optional

from openai_functools.function_spec import FunctionSpec
from openai_functools.metadata_generator import \
    extract_openai_function_metadata


class FunctionsOrchestrator:
    """
    Orchestrates the functions used in the OpenAI function calling models.
    """

    def __init__(self, functions: Optional[List[Callable]] = None) -> None:
        """
        Initializes the FunctionsOrchestrator with an optional list of functions.

        Args:
            functions (Optional[List[Callable]]): A list of functions to be registered.
        """
        self._functions = []
        self._function_specs = []

        if functions is not None:
            for function in functions:
                self._add_function(function)

    @property
    def functions(self) -> List[Callable]:
        """
        Returns the list of registered functions.

        Returns:
            List[Callable]: The list of registered functions.
        """
        return self._functions

    @functions.setter
    def functions(self, functions: List[Callable]) -> None:
        """
        Sets the list of registered functions.

        Args:
            functions (List[Callable]): A list of functions to be registered.
        """
        for function in functions:
            self._add_function(function)

    @property
    def function_specs(self) -> List[FunctionSpec]:
        """
        Returns the list of function specifications for the registered functions.

        Returns:
            List[FunctionSpec]: The list of function specifications.
        """
        return self._function_specs

    def register(self, function: Callable) -> None:
        """
        Registers a function.

        Args:
            function (Callable): The function to be registered.
        """
        self._add_function(function)

    def register_all(self, functions: List[Callable]) -> None:
        """
        Registers a list of functions.

        Args:
            functions (List[Callable]): The list of functions to be registered.
        """

        for function in functions:
            self._add_function(function)

    def _add_function(self, function: Callable) -> None:
        if not callable(function):
            raise TypeError(f'Function "{function}" is not callable.')

        if self._functions is None:
            self._functions = []
            self._function_specs = []

        matching_function = self._get_matching_function(function.__name__)

        if matching_function is not None:
            raise ValueError(f'Function "{function.__name__}" is already registered.')

        self._functions.append(function)
        self._function_specs.append(self._create_function_spec(function))

    def function(self, func: Optional[Callable] = None):
        """
        Registers a function if provided, otherwise returns a decorator for function registration.

        Args:
            func (Optional[Callable]): The function to be registered, if provided.

        Returns:
            Callable: The registered function or a decorator for function registration.
        """
        if func is not None:
            self.register(func)
            return func

        def wrapper(f):
            self.register(f)
            return f

        return wrapper

    def call_function(self, openai_response: dict) -> dict:
        """
        Calls a function based on the OpenAI response.

        Args:
            openai_response (dict): The OpenAI response containing the function call information.

        Returns:
            dict: The responses from the called function.
        """
        response_message = openai_response["choices"][0]["message"]

        if function_call := response_message.get("function_call"):
            function_name = function_call["name"]
            function_args = json.loads(function_call["arguments"])
            function = self._get_matching_function(function_name)

            if function is None:
                raise ValueError(
                    f'Function "{function_name}" is not '
                    f"registered with the orchestrator."
                )

            return function(**function_args)
        else:
            raise ValueError(
                f'Function call information not found in response message "{response_message}".'
            )

    def _get_matching_function(self, function_name: str) -> Optional[Callable]:
        """
        Returns the function that matches the provided function name, if it exists.

        Args:
            function_name (str): The name of the function to be retrieved.

        Returns:
            Optional[Callable]: The matching function, or None if no match is found.
        """
        for spec in self._function_specs:
            if spec.name == function_name:
                return spec.func_ref
        return None

    def _create_function_specs(self, functions: List[Callable]) -> List[FunctionSpec]:
        """
        Creates function specifications for a list of functions.

        Args:
            functions (List[Callable]): The list of functions for which to create specifications.

        Returns:
            List[FunctionSpec]: The list of created function specifications.
        """
        return [self._create_function_spec(function) for function in functions]

    @staticmethod
    def _create_function_spec(function: Callable) -> FunctionSpec:
        """
        Creates a function specification for a function.

        Args:
            function (Callable): The function for which to create a specification.

        Returns:
            FunctionSpec: The created function specification.
        """
        return FunctionSpec(
            func_ref=function, parameters=extract_openai_function_metadata(function)
        )

    @property
    def function_descriptions(self) -> List[Dict[str, Any]]:
        """
        Returns the descriptions of the registered functions.

        Returns:
            List[Dict[str, Any]]: The list of function descriptions.
        """
        return [spec.parameters for spec in self._function_specs]

    def create_function_descriptions(
        self, selected_functions: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Creates descriptions for the selected functions.

        Args:
            selected_functions (Optional[List[str]]): The list of selected function names. If None, descriptions for all registered functions are created.

        Returns:
            List[Dict[str, Any]]: The list of created function descriptions.
        """
        specs = (
            self._function_specs
            if selected_functions is None
            else [
                spec for spec in self._function_specs if spec.name in selected_functions
            ]
        )
        return [spec.parameters for spec in specs]
