from database.operations import select
from database.connection import DBContextManager

from flask import session
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def model_route(sql_provider, context: dict):
    today = datetime.now()
    min_date = (today + timedelta(days=1)).strftime("%Y-%m-%d")  # Завтрашний день
    max_date = (today + relativedelta(months=1)).strftime("%Y-%m-%d")  # Через месяц
    min_date_count = (today + timedelta(days=1)).date()  # Завтрашний день
    max_date_count = (today + relativedelta(months=1)).date()  # Через месяц

    time_options = generate_time_options(10, 21, 30)
    booked_dates = get_booked_dates(sql_provider, context,
                                    (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
                                    (datetime.now() + relativedelta(months=1)).strftime("%Y-%m-%d"))
    dates = {
        "min_date": min_date,
        "max_date": max_date,
        "time_options": time_options,
        "booked_dates": booked_dates,
        "error": None
    }

    if context['action'] == 'GET':
        return dates
    else:
        # Проверяем, занята ли выбранная дата и количество мест
        if context['selected_date'] in booked_dates and booked_dates[context['selected_date']] == int(
                context['hall_id']):
            dates['error'] = "В выбранную вами дату зал на рассчитываемое количество человек уже занят. " \
                    "Пожалуйста, выберите другую дату или измените количество человек посадки."
            return dates

        datetime_obj = datetime.strptime(f"{context['selected_date']} {context['selected_time']}", "%Y-%m-%d %H:%M")
        mysql_datetime = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
        if int(context['hall_id']) == 1:
            place_amount = 50
        elif int(context['hall_id']) == 2:
            place_amount = 30
        elif int(context['hall_id']) == 3:
            place_amount = 10
        else:
            place_amount = 18

        _sql = sql_provider.get(
            'make_order.sql',
            {'banquet_time': mysql_datetime,
             'expected_place_amount': place_amount,
             'idhall': context['hall_id'],
             'order_status': "В обработке",
             'client_phone': context['client_phone'],
             'user_id': session.get('user_id')}
        )
        with DBContextManager(context['db_config']) as cursor:
            cursor.execute(_sql)
        return dates


def generate_time_options(start_hour, end_hour, step_minutes):
    # Генерирует список времени от start_hour до end_hour с шагом в step_minutes.
    time_options = []
    current_time = datetime.strptime(f"{start_hour}:00", "%H:%M")
    end_time = datetime.strptime(f"{end_hour}:00", "%H:%M")
    while current_time <= end_time:
        time_options.append(current_time.strftime("%H:%M"))
        current_time += timedelta(minutes=step_minutes)
    return time_options


def get_booked_dates(sql_provider, context, tomorrow_date, next_month_date):
    # Даты, которые уже заняты
    _sql = sql_provider.get(
        'select_booked_dates.sql',
        {'tomorrow_date': tomorrow_date,
         'next_month_date': next_month_date}
    )
    dates = []
    halls = []
    with DBContextManager(context['db_config']) as cursor:
        cursor.execute(_sql)
        results = cursor.fetchall()
        for row in results:
            dates.append(row[0].strftime("%Y-%m-%d"))
            halls.append(row[1])
    return dict(zip(dates, halls))
