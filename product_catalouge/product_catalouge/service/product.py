

class Attribute:
    """docstring for Attribute."""
    def __init__(self, label, type, is_required):
        self.label = label
        self.type = type
        self.is_required = is_required
        self.value = None


class ProductType:
    """docstring for ProductType."""
    def __init__(self, name, description, gneral_attributes, variants_attributes):
        ...


class Category:
    """docstring for Category."""
    def __init__(self, name, description, sub_categories):
        ...


class Variant:
    def __init__(self, Name, sku, options, price, stock, media):
        ...


class Product:
    def __init__(self, name, description, product_type, category, media):
        ...