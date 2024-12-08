import os
from flask import Blueprint, request, render_template, session, redirect, url_for, current_app

from database.sql_provider import SQLProvider
from authorisation.model_route import model_route


auth_blueprint = Blueprint('bp_auth', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@auth_blueprint.route('/', methods=['GET', 'POST'])
def start_auth():
    if request.method == 'GET':
        return render_template('input_login.html', message='')
    else:
        if not request.form.get('login', '') or not request.form.get('password', ''):
            return render_template('input_login.html', message='Повторите ввод')

        return model_route(current_app.config['db_config'], provider, request)
