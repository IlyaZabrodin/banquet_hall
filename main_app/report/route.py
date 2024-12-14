import os
from datetime import datetime
from flask import Flask, render_template, Blueprint, current_app, request, session
from database.sql_provider import SQLProvider
from access import login_required
from .model_route import model_route

blueprint_report = Blueprint('bp_report', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_report.route('/', methods=['GET'])
@login_required(['director', 'hall_admin'])
def start_report():
    session['current_year'] = datetime.now().year
    context = {
        "year": session['current_year'],
        "u_group": session.get('user_group')
    }
    return render_template("report_form.html", context=context)


@blueprint_report.route('/', methods=['POST'])
@login_required(['director', 'hall_admin'])
def report_handler_result():
    info = model_route(db_config=current_app.config['db_config'], sql_provider=provider, request=request)
    if info.id_rep == 2:
        context = {
            "year": session['current_year'],
            "u_group": session.get('user_group'),
            "error_message": info.error_message
        }
        return render_template("report_form.html", context=context)
    return render_template(f"product_report.html", context=info)
