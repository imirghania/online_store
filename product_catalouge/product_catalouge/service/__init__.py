from typing import Protocol

class Service(Protocol):
    def create(self):
        ...
    
    def get_by_id(self):
        ...