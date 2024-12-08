import os
from flask import Blueprint, render_template, request, session, redirect, url_for, current_app

from database.sql_provider import SQLProvider
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
        "action": request.method,
        "error": None
    }

    if request.method == 'GET':
        dates = model_route(sql_provider=provider, context=context, request=request)
        return render_template('make_order_form.html', min_date=dates['min_date'], max_date=dates['max_date'],
                               time_options=dates['time_options'], booked_dates=dates['booked_dates'],
                               error=context['error'])
    elif request.method == 'POST':
        dates = model_route(sql_provider=provider, context=context, request=request)
        if context['error'] is None:
            return redirect(url_for('menu_choice'))
        else:
            return render_template('make_order_form.html', min_date=dates['min_date'], max_date=dates['max_date'],
                                   time_options=dates['time_options'], booked_dates=dates['booked_dates'],
                                   error=context['error'])
