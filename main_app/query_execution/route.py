import os
from flask import Blueprint, render_template, request, session, redirect, current_app
from datetime import datetime, timedelta

from database.sql_provider import SQLProvider
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
            session["query_code"] = request.args.get('query_code', default=None, type=int)
            return render_template('query_form_workload.html', query_code=session["query_code"])
        else:
            if request.args.get('order_id', default=None, type=int):
                sql = provider.get('show_order_dishes.sql', dict(order_id=request.args.get('order_id', default=None, type=int)))
                render_data = select_dict(current_app.config['db_config'], sql)

                return render_template(
                    'order_out.html',
                    render_data=render_data
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
        empty_code = 0
        if len(hall_id) == 0:
            empty_code = 1
        if session["query_code"] == 1:
            sql = provider.get('show_hall_workload.sql', dict(hall_id=hall_id, tomorrow_date=(
                    datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")))
        elif session["query_code"] == 2:
            sql = provider.get('show_hall_profit.sql', dict(hall_id=hall_id, order_status="Завершен", date_month_ago=(
                    datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")))
        render_data = select_dict(current_app.config['db_config'], sql)

        return render_template(
            'query_out.html',
            render_data=render_data,
            status_code=1,
            query_code=session["query_code"],
            empty_code=empty_code
        )
