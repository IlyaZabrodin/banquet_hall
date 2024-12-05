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
        price, balance = model_route(sql_provider=provider, context=context)
        message = None

        if price[0]['result'] > balance[0]['user_balance']:
            message = "Недостаточно средств. Пополните баланс."
        session['order_status'] = price[0]['order_status']
        session["diff"] = balance[0]['user_balance'] - price[0]['result']

        return render_template('payment_form.html', price=price[0]['result'], balance=balance[0]['user_balance'],
                               order_id=context['order_id'], message=message)

    elif request.method == 'POST':
        context["order_status"] = session.get('order_status')
        context["diff"] = session.get('diff')
        model_route(sql_provider=provider, context=context)
        return redirect(url_for('menu_choice'))
