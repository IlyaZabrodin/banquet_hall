from database.operations import select_dict, update
from pymysql import OperationalError
from flask import session


def model_route(sql_provider, context: dict):

    if context['action'] == 'GET':
        price_sql = sql_provider.get('find_price.sql', dict(order_id=context["order_id"]))
        price = select_dict(context['db_config'], price_sql)
        balance_sql = sql_provider.get('find_balance.sql', dict(user_id=context["user_id"]))
        balance = select_dict(context['db_config'], balance_sql)
        message = None

        if price[0]['result'] > balance[0]['user_balance']:
            message = "Недостаточно средств. Пополните баланс."
        session['order_status'] = price[0]['order_status']
        session["diff"] = balance[0]['user_balance'] - price[0]['result']

        return price[0]['result'], balance[0]['user_balance'], context['order_id'], message
    else:
        context["order_status"] = session.get('order_status')
        context["diff"] = session.get('diff')
        if context["order_status"] == "Подтвержден":
            order_status = "Полностью оформлен"
        elif context["order_status"] == "Ждет оплаты":
            order_status = "Завершен"
        _sql = sql_provider.get('update_price.sql', dict(order_id=context["order_id"], order_status=order_status))
        res = update(context["db_config"], _sql)
        if not res:
            raise OperationalError("Status order not updated")
        _sql = sql_provider.get('update_balance.sql', dict(user_id=context["user_id"], diff=context["diff"]))
        res = update(context["db_config"], _sql)
        if not res:
            raise OperationalError("Balance user not updated")
