from database.operations import select_dict, update
from pymysql import OperationalError


def model_route(sql_provider, context: dict):

    if context['action'] == 'GET':
        price_sql = sql_provider.get('find_price.sql', dict(order_id=context["order_id"]))
        price = select_dict(context['db_config'], price_sql)
        balance_sql = sql_provider.get('find_balance.sql', dict(user_id=context["user_id"]))
        balance = select_dict(context['db_config'], balance_sql)
        return price, balance
    else:
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
