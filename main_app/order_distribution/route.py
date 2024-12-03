import os
from flask import Blueprint, render_template, request, session, redirect, url_for, current_app

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from database.sql_provider import SQLProvider
from database.connection import DBContextManager
from database.operations import select
from access import login_required
from .model_route import model_route


blueprint_order_distribute = Blueprint(
    'bp_order_distribute',
    __name__,
    template_folder='templates'
)

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_order_distribute.route('/', methods=['GET', 'POST'])
@login_required(['hall_admin'])
def order_distribute():
    context = {
        "order_id": request.args.get('order_id'),
        "order_time": request.args.get('order_time'),
        "client_phone": request.args.get('client_phone'),
        "db_config": current_app.config['db_config'],
        "action": request.method
    }

    if request.method == 'GET':
        render_data = model_route(sql_provider=provider, context=context)
        return render_template('distribution_form.html', render_data=render_data,
                               phone=context['client_phone'], id=context['order_id'])
    elif request.method == 'POST':
        context['manager_id'] = request.form.get('manager_id')
        context['order_id'] = request.form.get('order_id')
        context['order_status'] = 'Подтвержден'
        model_route(sql_provider=provider, context=context)
        return redirect(url_for('menu_choice'))
