import json
from pathlib import Path
from flask import Flask, render_template, request, session, redirect

from authorisation.route import auth_blueprint
from query_execution.route import query_blueprint
from report.route import blueprint_report
from order_making.route import blueprint_order_make
from making_dish_list.route import blueprint_dish_list_make
from access import login_required
from user_properties import Properties

app = Flask(__name__)

app.register_blueprint(auth_blueprint, url_prefix='/authorisation')
app.register_blueprint(query_blueprint, url_prefix='/query_form')
app.register_blueprint(blueprint_report, url_prefix='/report')
app.register_blueprint(blueprint_order_make, url_prefix='/order_making')
app.register_blueprint(blueprint_dish_list_make, url_prefix='/dish_list_making')
app.secret_key = 'SuperKey'

project_path = Path(__file__).resolve().parent
app.config['db_config'] = json.load(open(project_path / 'configs/db.json'))


@app.route('/')
@login_required()
def menu_choice():
    user = Properties(session.get('user_id'), session.get('user_group'))
    if session.get('user_group') == 'client':
        return user.show_client()
    elif session.get('user_group') == 'manager':
        return user.show_manager()
    elif session.get('user_group') == 'director':
        return user.show_director()
    elif session.get('user_group') == 'hall_admin':
        return user.show_hall_admin()


@app.route('/access_fail')
@login_required()
def access_fail_handler():
    return render_template('access_error.html')


@app.route('/exit')
@login_required()
def logout_handler():
    session.clear()
    return render_template('exit.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
