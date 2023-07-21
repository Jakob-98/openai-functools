import json
from typing import List, Dict, Union, Any, Optional, Callable
from dataclasses import dataclass
import openai

@dataclass
class FunctionSpec:
    func_ref: Callable
    parameters: Dict[str, Any]

    @property
    def name(self) -> str:
        return self.func_ref.__name__

class OpenAIService:
    def __init__(self, openai: Any, model: str = 'gpt-3.5-turbo-0613', function_specs: List[FunctionSpec] = None):
        self.openai = openai
        self.model = model
        self.function_specs = function_specs if function_specs is not None else []

    def call_function(self, messages: List[Dict[str, str]], function_call: str = 'auto') -> Any:
        functions = [spec.parameters for spec in self.function_specs]

        response = self.openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            functions=functions,
            function_call=function_call,
        )

        response_message = response['choices'][0]['message']
        if response_message.get('function_call'):
            function_name = response_message['function_call']['name']
            function_args = json.loads(response_message['function_call']['arguments'])

            for spec in self.function_specs:
                if spec.name == function_name:
                    function_response = spec.func_ref(**function_args)
                    try:
                        if not isinstance(function_response, str):
                            function_response = str(function_response)
                    except Exception as e:
                        function_response = repr(function_response)
                    messages.append(response_message)
                    messages.append({'role': 'function', 'name': function_name, 'content': function_response})
                    print(messages)
                    second_response = self.openai.ChatCompletion.create(
                        model=self.model,
                        messages=messages,
                    )
                    return second_response

            raise ValueError(f'Function "{function_name}" not implemented.')
        
        return response

