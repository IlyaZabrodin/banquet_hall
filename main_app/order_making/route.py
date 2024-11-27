import os
from flask import Blueprint, render_template, request, session, redirect, current_app

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from database.sql_provider import SQLProvider
from database.connection import DBContextManager
from access import login_required


blueprint_order_make = Blueprint(
    'bp_order_make',
    __name__,
    template_folder='templates'
)

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_order_make.route('/', methods=['GET', 'POST'])
@login_required(['client'])
def order_make():
    if request.method == 'GET':
        today = datetime.now()
        min_date = (today + timedelta(days=1)).strftime("%Y-%m-%d")  # Завтрашний день
        max_date = (today + relativedelta(months=1)).strftime("%Y-%m-%d")  # Через месяц
        min_date_count = (today + timedelta(days=1)).date()  # Завтрашний день
        max_date_count = (today + relativedelta(months=1)).date()  # Через месяц

        time_options = generate_time_options(10, 21, 30)
        booked_dates = get_booked_dates((datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
                                        (datetime.now() + relativedelta(months=1)).strftime("%Y-%m-%d"))

        # Генерируем список всех дат в диапазоне
        all_dates = [
            (min_date_count + timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range((max_date_count - min_date_count).days + 1)
        ]

        # Фильтруем доступные даты, исключая занятые
        available_dates = [date for date in all_dates if date not in booked_dates]

        return render_template('make_order_form.html', min_date=min_date, max_date=max_date,
                               time_options=time_options, available_dates=available_dates)
    elif request.method == 'POST':
        prod_category = request.form.get('product-category', '')
        sql_statement = provider.get(
            'find_product_category.sql',
            {'prod_category': prod_category}
        )

        render_data = find_product_by_category(current_app.config['db_config'], sql_statement)

        return render_template(
            'query_out.html',
            render_data=render_data
        )


def generate_time_options(start_hour, end_hour, step_minutes):
    # Генерирует список времени от start_hour до end_hour с шагом в step_minutes.
    time_options = []
    current_time = datetime.strptime(f"{start_hour}:00", "%H:%M")
    end_time = datetime.strptime(f"{end_hour}:00", "%H:%M")
    while current_time <= end_time:
        time_options.append(current_time.strftime("%H:%M"))
        current_time += timedelta(minutes=step_minutes)
    return time_options


def get_booked_dates(tomorrow_date, next_month_date):
    # Даты, которые уже заняты
    sql = provider.get(
        'select_booked_dates.sql',
        {'tomorrow_date': tomorrow_date,
         'next_month_date': next_month_date}
    )
    with DBContextManager(current_app.config['db_config']) as cursor:
        cursor.execute(sql)
        results = cursor.fetchall()
        dates = [row[0].strftime("%Y-%m-%d") for row in results]
    return dates


def find_product_by_category(db_conf, sql):
    with DBContextManager(db_conf) as cursor:
        cursor.execute(sql)
        schema = [column[0] for column in cursor.description]
        result = [dict(zip(schema, row)) for row in cursor.fetchall()]

    render_data = {
        'status': True if result else False,
        'data': result
    }
    return render_data
