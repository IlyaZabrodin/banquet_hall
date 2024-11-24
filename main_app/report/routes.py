import os
from flask import Blueprint, render_template, request, session, redirect, current_app

from database.sql_provider import SQLProvider
from database.connection import DBContextManager
from access import login_required


blueprint_report = Blueprint('bp_report', __name__, template_folder='templates')

# provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_report.route('/', methods=['GET', 'POST'])
@login_required
def start_report():
    if request.method == 'GET':
        return render_template('report_menu.html')
    elif request.method == 'POST':
        month = request.form.get('month', '')
        print(month)
        print(111)
        # sql_statement = provider.get(
        #     'find_product_category.sql',
        #     {'prod_category': prod_category}
        # )
        #
        # render_data = find_product_by_category(current_app.config['db_config'], sql_statement)
        #
        # return render_template(
        #     'query_out.html',
        #     render_data=render_data
        # )


def show_rep_option(db_conf, sql):
    with DBContextManager(db_conf) as cursor:
        cursor.execute(sql)
        schema = [column[0] for column in cursor.description]
        result = cursor.fetchall()

    render_data = {
        'status': True if result else False,
        'data': schema
    }
    return render_data
