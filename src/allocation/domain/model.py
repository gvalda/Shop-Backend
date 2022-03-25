class BaseModel:
    pass


class OrderLine(BaseModel):
    def __init__(self, sku, quantity, order_id):
        self.sku = sku
        self.quantity = quantity
        self.order_id = order_id

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}<{self.sku}>'

    @property
    def serialize(self):
        return {
            'sku': self.sku,
            'quantity': self.quantity,
            'order_id': self.order_id,
        }


class Product(BaseModel):
    def __init__(self, sku, quantity):
        self.sku = sku
        self.quantity = quantity
        self._allocations = set()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}<{self.sku}>'

    def allocate(self, order_line: OrderLine):
        self._allocations.add(order_line)
