import os
from database.operations import delete
from database.sql_provider import SQLProvider


def cancel_order(db_config, order_id):
    provider = SQLProvider(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'sql'))
    _sql = provider.get('clear_client_order.sql', dict(order_id=order_id))
    print(_sql)
    res1 = delete(db_config, _sql)
    _sql = provider.get('clear_dish_list.sql', dict(order_id=order_id))
    res2 = delete(db_config, _sql)
    return res1, res2
