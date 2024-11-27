import os
from flask import Blueprint, render_template, request, session, redirect, current_app

from database.sql_provider import SQLProvider
from database.operations import select
from database.connection import DBContextManager
from access import login_required


blueprint_dish_list_make = Blueprint(
    'bp_dish_list_make',
    __name__,
    template_folder='templates'
)

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_dish_list_make.route('/', methods=['GET', 'POST'])
@login_required(['client'])
def dish_list_make():
    if request.method == 'GET':
        sql = provider.get('show_menu.sql')
        result, schema = select(current_app.config['db_config'], sql)
        render_data = {
            'status': True if result else False,
            'data': [i for i in result]
        }
        # portions = [0, 0, 0]
        # return render_template('show_menu.html', render_data=render_data, portions=portions)
        return render_template('show_menu.html', render_data=render_data)

