from dataclasses import dataclass
from typing import Any, Callable, Dict


@dataclass
class FunctionSpec:
    func_name: str
    func_ref: Callable
    parameters: Dict[str, Any]

    @property
    def name(self) -> str:
        return self.func_name
