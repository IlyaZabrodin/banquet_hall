import os
from flask import Blueprint, render_template, request, session, redirect, current_app
from datetime import datetime, timedelta

from database.sql_provider import SQLProvider
from database.connection import DBContextManager
from database.operations import select_dict
from access import login_required

query_blueprint = Blueprint(
    'bp_query',
    __name__,
    template_folder='templates'
)

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@query_blueprint.route('/', methods=['GET', 'POST'])
@login_required(['hall_admin', 'client', 'manager'])
def form_render():
    if request.method == 'GET':
        if session.get('user_group') in ['hall_admin']:
            return render_template('query_form_workload.html')
        else:
            if request.args.get('order_id', default=None, type=int):
                sql = provider.get('show_order_dishes.sql', dict(order_id=request.args.get('order_id', default=None, type=int)))
                render_data = select_dict(current_app.config['db_config'], sql)

                return render_template(
                    'order_out.html',
                    render_data=render_data,
                    status_code=1
                )
            else:
                sql = provider.get('show_menu.sql')
                render_data = select_dict(current_app.config['db_config'], sql)

                return render_template(
                    'query_out.html',
                    render_data=render_data,
                    status_code=2
                )
    elif request.method == 'POST':
        hall_id = request.form.get('hall_id', '')
        sql = provider.get('show_hall_workload.sql', dict(hall_id=hall_id,
                                                          tomorrow_date=(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")))
        render_data = select_dict(current_app.config['db_config'], sql)

        return render_template(
            'query_out.html',
            render_data=render_data,
            status_code=1
        )


def find_product_by_category(db_conf, sql):
    with DBContextManager(db_conf) as cursor:
        cursor.execute(sql)
        schema = [column[0] for column in cursor.description]
        result = [dict(zip(schema, row)) for row in cursor.fetchall()]

    render_data = {
        'status': True if result else False,
        'data': result
    }
    return render_data
