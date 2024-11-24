
import os, json
from datetime import datetime, timedelta
from flask import Flask, render_template, Blueprint, current_app, request, session
from access import group_required
from database.sql_provider import SQLProvider
from .model_route import model_route

blueprint_report = Blueprint('report_bp', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))
# error_list = []
# with open('./data/bp_report/error_list.json') as f:
#     error_list = json.load(f)
# print(f"\nerror_list = {error_list}")
# print(f"type error_list = {type(error_list)}\n")



@blueprint_report.route('/', methods=['GET'])
def report_index():
    context = {
        "year": session['current_year']
    }
    return render_template("main.html", context=context)


@blueprint_report.route('/', methods=['POST'])
def report_handler_result():
    report_list = [
        {'rep_id': '1', 'proc_name': 'staff_report', 'sql':'staff.sql'},
        {'rep_id': '2', 'proc_name': 'public.write_to_product_report', 'sql':'product.sql'}
    ]
    print()
    print(f"request.form = {list(request.form)}")
    print()
    for report in report_list:
        if request.form['report_choice'] == report['rep_id']:
           context = report
           break
    context["db_config"] = current_app.config['db_config']
    context['month'] = request.form['month_choice']
    context['year'] = request.form['year_choice']
    context['action'] = request.form['action']

    info = model_route(sql_provider=provider, context=context)
    print()
    print(f"info = {info}")
    print()

    return render_template(f"product_report.html", context=info)


    # if request.form['action'] == 'create':
    #     pass
    # else:
    #     info = model_route(sql_provider=provider, context=context)
    #     context['results'] = info.result
    #     if info.code_error == 1:
    #         info.is_exists = False
    #         info.error_message = error_list['view']
    #         context["error_message"] = error_list['view']
            # context["is_exists"] = False
    


    
    # result_list = (request.form['reuslt'])
    # for i, item in enumerate(result_list, start=1):
    #     param = "param"+str(i)
    #     context["result"][param]=item
    

    print()
    print(f'request.form["year"] = {request.form["year"]}')
    print(f'request.form["procedure_name"] = {request.form["procedure_name"]}')
    print(f'request.form["sql"] = {request.form["sql"]}')
    print(f'context["sql_name"] = {context["sql_name"]}')
    print(f'request.form["button"] = {request.form["button"]}')
    print()

    return render_template("report.html", context=context)
    # if info.code_error == 1:
    #     info.is_exists = False
    #     info.error_message = error_list[key]
    # print(f"info.result = {info.result}")
    # page = key + ".html"
   
    # if key == "last_registration":
    #     # res = context["result"]
    #     # date_object = datetime.strptime(f"{res}", "%Y-%m-%d").date()
    #     # date_object += timedelta(days=1)
    #     # context["result"] = (request.form[key], date_object.strftime('%Y-%m-%d'))
    #     if context["result"]['param1'] == '':
    #         context["result"]['param1'] = '1970-01-01'
    #     if context["result"]['param2'] == '':
    #         context["result"]['param2'] = datetime.now().strftime('%Y-%m-%d')


    # return render_template(page, context=info)
