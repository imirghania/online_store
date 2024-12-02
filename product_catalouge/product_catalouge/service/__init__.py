

class ProductRepository:
    def __init__(self, session):
        self.session = session
    
    def add(self, items):
        ...

    def _get(self, id_):
        ...

    def get(self, id_):
        ...

    def list(self, limit=None, **filters):
        ...

    def update(self, id_, **payload):
        ...

    def delete(self, id_):
        ...