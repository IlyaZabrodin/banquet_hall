from dataclasses import dataclass
from database.connection import DBContextManager
from flask import session, redirect, url_for, request
from pymysql import OperationalError
from database.operations import select_dict
from database.operations import update
from cache.wrapper import fetch_from_cache


@dataclass
class ProductInfoResponse:
    result: tuple
    error_message: str
    status: bool


def model_route_transaction_order(db_config: dict, sql_provider, basket: dict, price: int, order_id: int, role: str):
    total_amount = 0
    with DBContextManager(db_config) as cursor:
        for key, value in basket.items():
            _sql = sql_provider.get('insert_dish_list.sql',
                                    dict(dish_id=int(key), order_id=order_id, dish_amount=int(value)))
            try:
                cursor.execute(_sql)
            except OperationalError as error:
                print("error: ", "Dish is not appended")
                return False
            total_amount += int(value)

        if role == 'client':
            _sql = sql_provider.get('update_order.sql', dict(order_id=order_id, prepaid_expense=price,
                                                             dish_amount=total_amount))
        else:
            _sql = sql_provider.get('manager_update_order.sql', dict(order_id=order_id, add_pay=price,
                                                                     add_amount=total_amount,
                                                                     order_status="Ждет оплаты"))
        try:
            cursor.execute(_sql)
        except OperationalError as error:
            print("error: ", "Order list is not updated")
            return False

    result = tuple(str(order_id))
    return ProductInfoResponse(result, error_message="", status=True)


def model_basket_init(db_config, cache_config, sql_provider, request):
    order_id = request.args.get('order_id', default=None, type=int)
    err_code = request.args.get('err_code', default=None, type=int)
    role = session['user_group']
    if order_id:
        session['order_id'] = order_id

    cache_select_dict = fetch_from_cache('items_cached', cache_config)(select_dict)
    _sql = sql_provider.get('show_menu.sql')
    dishes = cache_select_dict(db_config, _sql)

    current_basket = session.get('basket', {})  # get basket or return default={}
    current_price = session.get('basket_price', 0)
    current_basket = form_basket(current_basket, db_config, sql_provider)

    return dishes, current_basket, current_price, role, err_code


def model_basket_main(db_config, sql_provider, request):
    if request.form.get('buy'):
        if not 'basket' in session:
            session['basket'] = dict()
            session['basket_price'] = 0
        _sql = sql_provider.get('select_dish.sql', dict(dish_id=int(request.form['dish_display'])))
        dish = select_dict(db_config, _sql)[0]
        current_basket = session.get('basket', {})

        # сессия поддерживает сериализацию через json, поэтому ключ может быть только строчкой
        # сессия не запоминает изменения значений по ключу, только добавление или удаление
        # поэтому нужно вручную указывать изменение сессии

        if str(dish['iddish']) in current_basket:
            prid = dish['iddish']
            amount = int(session['basket'][str(prid)])
            session['basket'][str(prid)] = str(amount + 1)
            session['basket_price'] += int(dish['dish_price'])
            session.modified = True
        else:
            prid = dish['iddish']
            session['basket'][str(prid)] = '1'
            session['basket_price'] += int(dish['dish_price'])
            session.modified = True

    if request.form.get('dish_increase'):
        # increasing count in basket
        _sql = sql_provider.get('select_dish.sql', dict(dish_id=int(request.form['dish_display'])))
        dish = select_dict(db_config, _sql)[0]
        amount = int(session['basket'][str(dish['iddish'])])
        session['basket'][str(dish['iddish'])] = str(amount + 1)
        session['basket_price'] += int(dish['dish_price'])
        session.modified = True

    if request.form.get('dish_reduce'):
        # decreasing count in basket
        _sql = sql_provider.get('select_dish.sql', dict(dish_id=int(request.form['dish_display'])))
        dish = select_dict(db_config, _sql)[0]
        amount = int(session['basket'][str(dish['iddish'])])
        if amount == 1:
            session['basket'].pop(str(dish['iddish']))
        else:
            session['basket'][str(dish['iddish'])] = str(amount - 1)
        session['basket_price'] -= int(dish['dish_price'])
        session.modified = True

    return redirect(url_for('bp_dish_list.basket_index'))


def model_save_order(db_config, sql_provider, request):
    role = request.args.get('role', default=None, type=str)
    current_basket = session.get('basket', {})
    current_price = session.get('basket_price', 0)
    order_id = session.get('order_id')
    result = model_route_transaction_order(db_config, sql_provider,
                                           current_basket, current_price, order_id, role)
    return result


def model_complete_order(db_config, sql_provider):
    order_id = session.get('order_id')
    _sql = sql_provider.get('complete_order.sql', dict(order_id=order_id, order_status="Завершен"))
    res = update(db_config, _sql)
    return res


def form_basket(current_basket: dict, db_config: dict,  sql_provider):
    basket = []
    for elem, quantity in current_basket.items():
        _sql = sql_provider.get('select_dish.sql', dict(dish_id=elem))
        dish = select_dict(db_config, _sql)[0]
        dish['amount'] = quantity
        basket.append(dish)
    return basket

