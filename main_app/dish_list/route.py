from flask import Blueprint, session, redirect, url_for, render_template, current_app, request
from database.sql_provider import SQLProvider
import os
from pymysql import OperationalError
from access import login_required
from dish_list.model_route import model_basket_init, model_basket_main, model_save_order, model_complete_order


blueprint_dish_list = Blueprint('bp_dish_list', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_dish_list.route('/', methods=['GET'])
@login_required(['client', 'manager'])
def basket_index():
    dishes, current_basket, current_price, role, err_code = model_basket_init(current_app.config['db_config'],
                                                                              current_app.config['cache_config'],
                                                                              provider, request)
    if err_code:
        return render_template('basket_dynamic.html', dishes=dishes, basket=current_basket, basket_price=current_price,
                               role=role, message="Запрос не выполнен")
    return render_template('basket_dynamic.html', dishes=dishes, basket=current_basket, basket_price=current_price,
                           role=role)


@blueprint_dish_list.route('/', methods=['POST'])
@login_required(['client', 'manager'])
def basket_main():
    return model_basket_main(current_app.config['db_config'], provider, request)


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
    if not session.get('basket', {}):
        return redirect(url_for('bp_dish_list.basket_index'))

    result = model_save_order(current_app.config['db_config'], provider, request)
    if result.status:
        clear_basket()
        if request.args.get('role', default=None, type=str) == 'client':
            return redirect(url_for('bp_payment.payment_form', order_id=session.get('order_id')))
        else:
            return redirect(url_for('menu_choice'))
    else:
        return redirect(url_for('bp_dish_list.basket_index', err_code=1))


@blueprint_dish_list.route('/complete_order')
@login_required(['manager'])
def complete_order():
    res = model_complete_order(current_app.config['db_config'], provider)
    if not res:
        raise OperationalError("Order list is not updated")
    return redirect(url_for('menu_choice'))
