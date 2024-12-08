import os
from flask import Blueprint, render_template, request, session, redirect, url_for, current_app

from database.sql_provider import SQLProvider
from access import login_required
from .model_route import model_route


blueprint_payment = Blueprint(
    'bp_payment',
    __name__,
    template_folder='templates'
)

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_payment.route('/', methods=['GET', 'POST'])
@login_required(['client'])
def payment_form():
    context = {
        "order_id": request.args.get('order_id', default=None, type=int),
        "user_id": session.get('user_id'),
        "db_config": current_app.config['db_config'],
        "action": request.method
    }

    if request.method == 'GET':
        price, balance, order_id, message = model_route(sql_provider=provider, context=context)
        return render_template('payment_form.html', price=price, balance=balance,
                               order_id=order_id, message=message)

    elif request.method == 'POST':
        model_route(sql_provider=provider, context=context)
        return redirect(url_for('menu_choice'))
