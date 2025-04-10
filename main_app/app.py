import json
from pathlib import Path
from flask import Flask, render_template, request, session, redirect, url_for, current_app
from pymysql.err import OperationalError
from datetime import datetime

from authorisation.route import auth_blueprint
from query_execution.route import query_blueprint
from report.route import blueprint_report
from order_making.route import blueprint_order_make
from dish_list.route import blueprint_dish_list
from order_distribution.route import blueprint_order_distribute
from payment.route import blueprint_payment
from access import login_required
from user_properties import Properties
from database.order_cancellation import cancel_order

app = Flask(__name__)

app.register_blueprint(auth_blueprint, url_prefix='/authorisation')
app.register_blueprint(query_blueprint, url_prefix='/query_form')
app.register_blueprint(blueprint_report, url_prefix='/report')
app.register_blueprint(blueprint_order_make, url_prefix='/order_making')
app.register_blueprint(blueprint_dish_list, url_prefix='/dish_list')
app.register_blueprint(blueprint_order_distribute, url_prefix='/order_distribution')
app.register_blueprint(blueprint_payment, url_prefix='/payment')
app.secret_key = 'SuperKey'

project_path = Path(__file__).resolve().parent
app.config['db_config'] = json.load(open(project_path / 'configs/db.json'))
app.config['procedures'] = json.load(open(project_path / 'configs/procedures.json'))
app.config['cache_config'] = json.load(open(project_path / 'configs/cache.json'))


@app.context_processor
def inject_global_vars():
    blueprint = request.blueprint
    context = {
        'cur_date': datetime.now().date(),
        'site_name': 'Banquet Hall System'
    }
    if blueprint not in ['auth_blueprint']:
        if 'user_id' in session:
            context['user_id'] = session['user_id']
            context['role'] = session['user_group']

    return context


@app.route('/')
@login_required()
def menu_choice():
    user = Properties(session.get('user_id'), session.get('user_group'))
    return user.show_template()


@app.route('/access_fail')
@login_required()
def access_fail_handler():
    return render_template('access_error.html')


@app.route('/exit')
@login_required()
def logout_handler():
    session.clear()
    return render_template('exit.html')


@app.route('/cancel-order', methods=['POST'])
@login_required(['client', 'manager'])
def cancel_order_handler():
    order_id = request.args.get('order_id', default=None, type=int)
    res1, res2 = cancel_order(current_app.config['db_config'], order_id)
    if not res1 or not res2:
        raise OperationalError("Dish lists not deleted")
    return redirect(url_for('menu_choice'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
