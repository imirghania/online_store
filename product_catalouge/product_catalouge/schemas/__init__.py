from typing import Protocol


class BaseSchema(Protocol):
    
    def dict(self):
        ...
