import json
from pathlib import Path

from flask import Flask, render_template, session

from auth.route import blueprint_auth
from report.route import blueprint_report
from query.route import blueprint_query
from market.route import blueprint_market
from access import login_required


app = Flask(__name__)
app.secret_key = 'SuperKey'

app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_query, url_prefix='/query_execution')
app.register_blueprint(blueprint_report, url_prefix='/report')
app.register_blueprint(blueprint_market, url_prefix='/order_making')

project_path = Path(__file__).resolve().parent
app.config['db_config'] = json.load(open(project_path / 'configs/db.json'))


@app.route('/')
@login_required
def menu_choice():
    return render_template('internal_user_menu.html' if session.get('user_group') else 'external_user_menu.html')


@app.route('/exit')
@login_required
def exit_func():
    session.clear()
    return render_template('exit.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
