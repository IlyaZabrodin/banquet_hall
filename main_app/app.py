import json
from pathlib import Path
from flask import Flask, render_template, request, session, redirect

from authorisation.routes import auth_blueprint
from query_execution.routes import query_blueprint
from report.routes import blueprint_report
from market.route import blueprint_market
from access import login_required

app = Flask(__name__)

app.register_blueprint(auth_blueprint, url_prefix='/authorisation')
app.register_blueprint(query_blueprint, url_prefix='/query_form')
app.register_blueprint(blueprint_report, url_prefix='/report')
app.register_blueprint(blueprint_market, url_prefix='/market')
app.secret_key = 'SuperKey'

project_path = Path(__file__).resolve().parent
app.config['db_config'] = json.load(open(project_path / 'configs/db.json'))


@app.route('/')
@login_required
def menu_choice():
    return render_template('internal_user_menu.html' if session.get('user_group') else 'external_user_menu.html')


@app.route('/exit')
@login_required
def logout_handler():
    session.clear()
    return render_template('exit.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
