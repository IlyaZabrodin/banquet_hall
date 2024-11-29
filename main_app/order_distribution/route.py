import os
from flask import Blueprint, render_template, request, session, redirect, url_for, current_app

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from database.sql_provider import SQLProvider
from database.connection import DBContextManager
from database.operations import select
from access import login_required


blueprint_order_distribute = Blueprint(
    'bp_order_distribute',
    __name__,
    template_folder='templates'
)

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_order_distribute.route('/', methods=['GET', 'POST'])
@login_required(['hall_admin'])
def order_distribute():
    order_id = request.args.get('param1')
    order_time = request.args.get('param2')
    client_phone = request.args.get('param3')

    sql = provider.get('search_managers.sql', dict(order_date=order_time))
    result, schema = select(current_app.config['db_config'], sql)
    render_data = {
        'status': True if result else False,
        'data': [i for i in result]
    }

    if request.method == 'GET':
        return render_template('distribution_form.html', render_data=render_data, phone=client_phone, id=order_id)
    elif request.method == 'POST':
        manager_id = request.form.get('manager_id')
        order_id = request.form.get('order_id')

        sql = provider.get(
            'set_manager.sql',
            {'manager_id': manager_id,
             'order_id': order_id,
             'order_status': "Подтвержден"}
        )
        with DBContextManager(current_app.config['db_config']) as cursor:
            cursor.execute(sql)
        return redirect(url_for('menu_choice'))
