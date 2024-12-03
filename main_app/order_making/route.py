import os
from flask import Blueprint, render_template, request, session, redirect, url_for, current_app

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from database.sql_provider import SQLProvider
from database.connection import DBContextManager
from access import login_required
from .model_route import model_route


blueprint_order_make = Blueprint(
    'bp_order_make',
    __name__,
    template_folder='templates'
)

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_order_make.route('/', methods=['GET', 'POST'])
@login_required(['client'])
def order_make():
    context = {
        "db_config": current_app.config['db_config'],
        "action": request.method
    }

    if request.method == 'GET':
        dates = model_route(sql_provider=provider, context=context)
        return render_template('make_order_form.html', min_date=dates['min_date'], max_date=dates['max_date'],
                               time_options=dates['time_options'], booked_dates=dates['booked_dates'],
                               error=dates['error'])
    elif request.method == 'POST':
        context['selected_date'] = request.form.get('date')
        context['hall_id'] = request.form.get('place_amount')
        context['selected_time'] = request.form.get('time')
        context['client_phone'] = request.form.get('phone')

        dates = model_route(sql_provider=provider, context=context)
        if dates['error'] is None:
            return redirect(url_for('menu_choice'))
        else:
            return render_template('make_order_form.html', min_date=dates['min_date'], max_date=dates['max_date'],
                                   time_options=dates['time_options'], booked_dates=dates['booked_dates'],
                                   error=dates['error'])
