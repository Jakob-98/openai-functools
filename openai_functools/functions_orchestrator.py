import json
from typing import Any, Callable, Dict, List, Optional

from openai_functools.function_spec import FunctionSpec
from openai_functools.metadata_generator import (
    construct_function_name,
    extract_openai_function_metadata,
)


class FunctionsOrchestrator:
    SUPPORTED_MODEL_VERSIONS = ["gpt-3.5-turbo", "text-davinci-002", "text-curie-003"]
=======
    """
    Orchestrates the functions used in the OpenAI function calling models.
    """

    _functions: Dict[str, FunctionSpec]

    def __init__(self, functions: Optional[List[Callable]] = None, model_version: Optional[str] = None) -> None:
        """
        Initializes the FunctionsOrchestrator with an optional list of functions and model version.

        Args:
            functions (Optional[List[Callable]]): A list of functions to be registered.
            model_version (Optional[str]): The version of the model to be used.
        """
        self._functions = {}
        self.model_version = model_version

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
        return self._functions.values()

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

    def register_instance(self, instance: Any) -> None:
        """
        Registers all methods of a single instance.

        Args:
            instance (Any): The instance whose methods are to be registered.
        """

        for method_name in dir(instance):
            method = getattr(instance, method_name)
            if not method_name.startswith("__") and callable(method):
                self._add_function(getattr(instance, method_name))

    def register_instances_all(self, instances: List[Any]):
        """
        Registers all methods of all instances.

        Args:
            instances (Any): The instances whose methods are to be registered.
        """

        for instance in instances:
            self.register_instance(instance)

    def _add_function(self, function: Callable) -> None:
        if not callable(function):
            raise TypeError(f'Function "{function}" is not callable.')

        function_name = construct_function_name(function)
        if function_name in self._functions:
            raise ValueError(f'Function "{function.__name__}" is already registered.')

        self._functions[function_name] = self._create_function_spec(function)

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

        if self.model_version not in self.SUPPORTED_MODEL_VERSIONS:
            raise ValueError(f'Model version "{self.model_version}" is not supported.')
        
        if function_call := response_message.get("function_call"):
            function_name = function_call["name"]
            function_args = json.loads(function_call["arguments"])
            function = self._functions[function_name]

            if function is None:
                raise ValueError(
                    f'Function "{function_name}" is not '
                    f"registered with the orchestrator."
                )
            return function.func_ref(**function_args)
        elif tool_calls := response_message.get("tool_calls"):
            function_responses = {}
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                function = self._functions[function_name]
                function_responses[tool_call.id] = function.func_ref(**function_args)
            return function_responses
        else:
            raise ValueError(
                f'Function call information not found in response message "{response_message}".'
            )

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
            func_name=construct_function_name(function),
            func_ref=function,
            parameters=extract_openai_function_metadata(function),
        )

    @property
    def function_descriptions(self) -> List[Dict[str, Any]]:
        """
        Returns the descriptions of the registered functions.

        Returns:
            List[Dict[str, Any]]: The list of function descriptions.
        """
        return [spec.parameters for spec in self._functions.values()]

    def create_function_descriptions(
        self, selected_functions: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Creates descriptions for the selected functions. This should be used when calling ChatCompletion.create with the functions argument.

        Args:
            selected_functions (Optional[List[str]]): The list of selected function names. If None, descriptions for all registered functions are created.

        Returns:
            List[Dict[str, Any]]: The list of created function descriptions.
        """
        specs = (
            self._functions.values()
            if selected_functions is None
            else [
                spec
                for spec in self._functions.values()
                if spec.name in selected_functions
            ]
        )
        return [spec.parameters for spec in specs]

    def create_tools_descriptions(
        self, selected_functions: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Creates descriptions for the selected functions. This should be used when calling ChatCompletion.create with the tools argument.

        Args:
            selected_functions (Optional[List[str]]): The list of selected function names. If None, descriptions for all registered functions are created.

        Returns:
            List[Dict[str, Any]]: The list of created tool descriptions.
        """
        specs = (
            self._functions.values()
            if selected_functions is None
            else [
                spec
                for spec in self._functions.values()
                if spec.name in selected_functions
            ]
        )
        return [{"type": "function", "function": spec.parameters} for spec in specs]
    def set_model_version(self, model_version: str) -> None:
        """
        Sets the model version.

        Args:
            model_version (str): The version of the model to be used.
        """
        if model_version not in self.SUPPORTED_MODEL_VERSIONS:
            raise ValueError(f'Model version "{model_version}" is not supported.')
        self.model_version = model_version
