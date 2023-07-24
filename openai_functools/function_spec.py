from dataclasses import dataclass
from typing import Any, Callable, Dict


@dataclass
class FunctionSpec:
    func_ref: Callable
    parameters: Dict[str, Any]

    @property
    def name(self) -> str:
        return self.func_ref.__name__
