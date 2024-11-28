import os
from datetime import datetime, timedelta
from flask import Flask, render_template, Blueprint, current_app, request, session
from database.sql_provider import SQLProvider
from access import login_required
from .model_route import model_route

blueprint_report = Blueprint('bp_report', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_report.route('/', methods=['GET'])
@login_required(['director'])
def start_report():
    session['current_year'] = datetime.now().year
    context = {
        "year": session['current_year']
    }
    return render_template("main.html", context=context)


@blueprint_report.route('/', methods=['POST'])
@login_required(['director'])
def report_handler_result():
    report_list = [
        {'rep_id': '1', 'proc_name': 'schema_1.SaleReport', 'sql': 'sales_report.sql'},
        {'rep_id': '2', 'proc_name': 'schema_1.OrderReport', 'sql': 'workers_report.sql'}
    ]

    for report in report_list:
        if request.form['report_choice'] == report['rep_id']:
            context = report
            break
    context["db_config"] = current_app.config['db_config']
    context['month'] = request.form['month_choice']
    context['year'] = request.form['year_choice']
    context['action'] = request.form['action']

    info = model_route(sql_provider=provider, context=context)

    return render_template(f"product_report.html", context=info)
