import os
from flask import Blueprint, render_template, request, session, redirect, url_for, current_app

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
    today = datetime.now()
    min_date = (today + timedelta(days=1)).strftime("%Y-%m-%d")  # Завтрашний день
    max_date = (today + relativedelta(months=1)).strftime("%Y-%m-%d")  # Через месяц
    min_date_count = (today + timedelta(days=1)).date()  # Завтрашний день
    max_date_count = (today + relativedelta(months=1)).date()  # Через месяц

    time_options = generate_time_options(10, 21, 30)
    booked_dates = get_booked_dates((datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
                                    (datetime.now() + relativedelta(months=1)).strftime("%Y-%m-%d"))

    if request.method == 'GET':
        return render_template('make_order_form.html', min_date=min_date, max_date=max_date,
                               time_options=time_options, booked_dates=booked_dates, error=None)
    elif request.method == 'POST':
        selected_date = request.form.get('date')
        hall_id = request.form.get('place_amount')

        selected_time = request.form.get('time')
        client_phone = request.form.get('phone')

        # Проверяем, занята ли выбранная дата и количество мест
        if selected_date in booked_dates and booked_dates[selected_date] == int(hall_id):
            error = "В выбранную вами дату зал на рассчитываемое количество человек уже занят. " \
                    "Пожалуйста, выберите другую дату или измените количество человек посадки."
            return render_template('make_order_form.html', min_date=min_date, max_date=max_date,
                                   time_options=time_options, booked_dates=booked_dates, error=error)

        datetime_obj = datetime.strptime(f"{selected_date} {selected_time}", "%Y-%m-%d %H:%M")
        mysql_datetime = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
        if int(hall_id) == 1:
            place_amount = 50
        elif int(hall_id) == 2:
            place_amount = 30
        elif int(hall_id) == 3:
            place_amount = 10
        else:
            place_amount = 18

        sql = provider.get(
            'make_order.sql',
            {'banquet_time': mysql_datetime,
             'expected_place_amount': place_amount,
             'idhall': hall_id,
             'order_status': "В обработке",
             'client_phone': client_phone,
             'user_id': session.get('user_id')}
        )
        with DBContextManager(current_app.config['db_config']) as cursor:
            cursor.execute(sql)
        return redirect(url_for('menu_choice'))


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
    dates = []
    halls = []
    with DBContextManager(current_app.config['db_config']) as cursor:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            dates.append(row[0].strftime("%Y-%m-%d"))
            halls.append(row[1])
    return dict(zip(dates, halls))


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
