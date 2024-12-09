from database.operations import select_dict, select
from flask import session
from datetime import datetime, timedelta


def model_route(sql_provider, db_config: dict, request):
    if request.method == 'GET':
        if session.get('user_group') in ['hall_admin']:
            session["query_code"] = request.args.get('query_code', default=None, type=int)
            if session["query_code"] in [1, 3]:
                sql = sql_provider.get('value_list_halls.sql')
            elif session["query_code"] == 2:
                sql = sql_provider.get('value_list_managers.sql',
                                       dict(current_date=(datetime.now()).strftime("%Y-%m-%d")))
            result, schema = select(db_config, sql)
            res = [i[0] for i in result]
            indexes = [i[1] for i in result] if session["query_code"] == 2 else []

            if session["query_code"] == 3:
                today = datetime.now()
                min_date = (today + timedelta(days=1)).strftime("%Y-%m-%d")  # Завтрашний день
                max_date = (today + timedelta(days=30)).strftime("%Y-%m-%d")  # Через месяц
                return res, min_date, max_date

            return res, indexes
        if request.args.get('order_id', default=None, type=int):
            sql = sql_provider.get('show_order_dishes.sql',
                                   dict(order_id=request.args.get('order_id', default=None, type=int)))
            render_data = select_dict(db_config, sql)
            return render_data, 0
        else:
            sql = sql_provider.get('show_menu.sql')
            render_data = select_dict(db_config, sql)
            return render_data, 2
    else:
        if session["query_code"] == 1:
            if request.form.get('hall_choice'):
                info = request.form['hall_choice']
            else:
                return {}, 1
            session['hall_choice'] = info
            sql = sql_provider.get('show_hall_workload.sql', dict(hall_id=info, tomorrow_date=(
                    datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")))
        elif session["query_code"] == 2:
            if request.form.get('manager_choice'):
                info = request.form['manager_choice']
            else:
                return {}, 1
            session['manager_choice'] = info
            sql = sql_provider.get('show_manager_orders.sql', dict(manager_id=info, current_date=(datetime.now()).strftime("%Y-%m-%d")))
        elif session["query_code"] == 3:
            if request.form.get('hall_choice'):
                info = request.form['hall_choice']
            else:
                return {}, 1
            session['hall_choice'] = info
            search_date = request.form.get('date')
            sql = sql_provider.get('check_hall_work.sql', dict(hall_id=info, search_date=search_date))
        render_data = select_dict(db_config, sql)
        return render_data, 0
