from flask import Blueprint, session, redirect, url_for, render_template, current_app, request
from database.sql_provider import SQLProvider
import os
from pymysql import OperationalError
from database.operations import select_dict
from database.operations import update
from dish_list.model_route import model_route_transaction_order
from access import login_required


blueprint_dish_list = Blueprint('bp_dish_list', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_dish_list.route('/', methods=['GET'])
@login_required(['client', 'manager'])
def basket_index():
    order_id = request.args.get('order_id', default=None, type=int)
    err_code = request.args.get('err_code', default=None, type=int)
    role = session['user_group']
    if order_id:
        session['order_id'] = order_id

    db_config = current_app.config['db_config']
    _sql = provider.get('show_menu.sql')
    dishes = select_dict(db_config, _sql)

    current_basket = session.get('basket', {})  # get basket or return default={}
    current_price = session.get('basket_price', 0)
    current_basket = form_basket(current_basket)

    if err_code:
        return render_template('basket_dynamic.html', dishes=dishes, basket=current_basket, basket_price=current_price,
                               role=role, message="Запрос не выполнен")
    return render_template('basket_dynamic.html', dishes=dishes, basket=current_basket, basket_price=current_price,
                           role=role)


@blueprint_dish_list.route('/', methods=['POST'])
@login_required(['client', 'manager'])
def basket_main():
    db_config = current_app.config['db_config']
    if request.form.get('buy'):
        if not 'basket' in session:
            session['basket'] = dict()
            session['basket_price'] = 0
        _sql = provider.get('select_dish.sql', dict(dish_id=int(request.form['dish_display'])))
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
        _sql = provider.get('select_dish.sql', dict(dish_id=int(request.form['dish_display'])))
        dish = select_dict(db_config, _sql)[0]
        amount = int(session['basket'][str(dish['iddish'])])
        session['basket'][str(dish['iddish'])] = str(amount + 1)
        session['basket_price'] += int(dish['dish_price'])
        session.modified = True

    if request.form.get('dish_reduce'):
        # decreasing count in basket
        _sql = provider.get('select_dish.sql', dict(dish_id=int(request.form['dish_display'])))
        dish = select_dict(db_config, _sql)[0]
        amount = int(session['basket'][str(dish['iddish'])])
        if amount == 1:
            session['basket'].pop(str(dish['iddish']))
        else:
            session['basket'][str(dish['iddish'])] = str(amount - 1)
        session['basket_price'] -= int(dish['dish_price'])
        session.modified = True

    return redirect(url_for('bp_dish_list.basket_index'))


@blueprint_dish_list.route('/clear_basket')
@login_required(['client', 'manager'])
def clear_basket():
    if session.get('basket', {}):
        session.pop('basket')
        session['basket_price'] = 0
    return redirect(url_for('bp_dish_list.basket_index'))


@blueprint_dish_list.route('/save_order')
@login_required(['client', 'manager'])
def save_order():
    role = request.args.get('role', default=None, type=str)

    if not session.get('basket', {}):
        return redirect(url_for('bp_dish_list.basket_index'))
    current_basket = session.get('basket', {})
    current_price = session.get('basket_price', 0)
    order_id = session.get('order_id')
    result = model_route_transaction_order(current_app.config['db_config'], provider,
                                           current_basket, current_price, order_id, role)
    if result.status:
        clear_basket()
        if role == 'client':
            return redirect(url_for('menu_choice'))
        else:
            return redirect(url_for('menu_choice'))
    else:
        return redirect(url_for('bp_dish_list.basket_index', err_code=1))


@blueprint_dish_list.route('/complete_order')
@login_required(['manager'])
def complete_order():
    db_config = current_app.config['db_config']
    order_id = session.get('order_id')

    _sql = provider.get('complete_order.sql', dict(order_id=order_id, order_status="Завершен"))
    res = update(db_config, _sql)
    if not res:
        raise OperationalError("Order list is not updated")
    return redirect(url_for('menu_choice'))


def form_basket(current_basket: dict):
    basket = []
    for elem, quantity in current_basket.items():
        _sql = provider.get('select_dish.sql', dict(dish_id=elem))
        dish = select_dict(current_app.config['db_config'], _sql)[0]
        dish['amount'] = quantity
        basket.append(dish)
    return basket
