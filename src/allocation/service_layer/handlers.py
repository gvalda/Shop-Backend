from allocation.service_layer import unit_of_work
from allocation.exceptions import InvalidSku
from allocation.domain import model


def allocate(
    sku: str,
    quantity: int,
    order_id: str,
    uow: unit_of_work.AbstractUnitOfWork
):
    with uow:
        product = uow.products.get(sku)
        if not product:
            raise InvalidSku(f'Invalid sku {sku}')
        order_line = model.OrderLine(sku, quantity, order_id)
        product.allocate(order_line)
        uow.commit()


def add_in_stock(
    sku: str,
    quantity: int,
    uow: unit_of_work.AbstractUnitOfWork
):
    with uow:
        product = uow.products.get(sku)
        if not product:
            product = model.Product(sku, 0)
        product.quantity += quantity
        uow.commit()


def order_allocations(
    order_id: str,
    uow: unit_of_work.AbstractUnitOfWork
):
    with uow:
        order_lines = uow.products.get_order_lines(order_id)
        order_lines_dict = [order_line.serialize for order_line in order_lines]
    return order_lines_dict
