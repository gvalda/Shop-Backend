from datetime import timedelta
from functools import update_wrapper

from flask import Flask, request, jsonify, current_app, make_response

from products.service_layer import handlers
from products.bootstrap import bootstrap
from products.enums import StatusCodes
from products import exceptions

app = Flask(__name__)

# TODO Create separete file for  cross domain


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        # f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


uow = bootstrap()


# @app.route('/products', methods=['POST'])
# def add_stock():
#     handlers.add_in_stock(
#         request.json['sku'],
#         request.json['quantity'],
#         uow
#     )
#     return 'OK', StatusCodes.OK_200


# @app.route('/allocations', methods=['POST'])
# def allocate_order():
#     try:
#         handlers.allocate(
#             request.json['sku'],
#             request.json['quantity'],
#             request.json['order_id'],
#             uow
#         )
#     except exceptions.InvalidSku as e:
#         return {'message': str(e)}, StatusCodes.BAD_REQUEST_400

#     return 'OK', StatusCodes.OK_200


# @app.route('/allocations/<order_id>', methods=['GET'])
# def get_allocations(order_id):
#     results = handlers.order_allocations(order_id, uow)
#     if not results:
#         return 'NOT FOUND', StatusCodes.NOT_FOUND_404
#     return jsonify(order_lines=results), StatusCodes.OK_200

@app.route('/products', methods=['GET'])
@crossdomain(origin="*")
def get_products():
    # TODO Read cross-domain sites from config file
    # TODO Make one list for safe sites
    results = handlers.get_all_products(uow)
    if not results:
        results = []
    return jsonify(products=results), StatusCodes.OK_200


@app.route('/products', methods=['POST'])
def add_product():
    # TODO Check if request contains sku, name and description
    handlers.add_product(
        request.json['sku'],
        request.json['name'],
        request.json['description'],
        uow
    )
    return "Created", StatusCodes.CREATED_201


@app.route('/products/<sku>', methods=['GET'])
@crossdomain(origin="*")
def get_product(sku):
    try:
        result = handlers.get_product(sku, uow)
    except exceptions.InvalidSku as e:
        return {'message': str(e)}, StatusCodes.BAD_REQUEST_400
    return jsonify(result), StatusCodes.OK_200
