from flask import Flask, request, jsonify

from allocation.service_layer import handlers
from allocation.bootstrap import bootstrap
from allocation.enums import StatusCodes
from allocation import exceptions

app = Flask(__name__)

uow = bootstrap()


@app.route('/products', methods=['POST'])
def add_stock():
    handlers.add_in_stock(
        request.json['sku'],
        request.json['quantity'],
        uow
    )
    return 'OK', StatusCodes.OK_200


@app.route('/allocations', methods=['POST'])
def allocate_order():
    try:
        handlers.allocate(
            request.json['sku'],
            request.json['quantity'],
            request.json['order_id'],
            uow
        )
    except exceptions.InvalidSku as e:
        return {'message': str(e)}, StatusCodes.BAD_REQUEST_400

    return 'OK', StatusCodes.OK_200


@app.route('/allocations/<order_id>', methods=['GET'])
def get_allocations(order_id):
    results = handlers.order_allocations(order_id, uow)
    if not results:
        return 'NOT FOUND', StatusCodes.NOT_FOUND_404
    return jsonify(order_lines=results), StatusCodes.OK_200
