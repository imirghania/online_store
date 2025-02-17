from dataclasses import dataclass
from typing import Protocol



@dataclass
class Model(Protocol):
    def dict(self):
        ...


@dataclass
class Domain(Protocol):
    def dict(self):
        ...
