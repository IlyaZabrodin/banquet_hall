from dataclasses import dataclass
from flask import session

from database.operations import insert_one
from database.operations import update
from pymysql import OperationalError


@dataclass
class ProductInfoRespronse:
    result: tuple
    error_message: str
    status: bool


def model_route_transaction_order(db_config: dict, sql_provider, basket: dict, price: int, order_id: int, role: str):
    total_amount = 0
    for key, value in basket.items():
        _sql = sql_provider.get('insert_dish_list.sql',
                                dict(dish_id=int(key), order_id=order_id, dish_amount=int(value)))
        result = insert_one(db_config, _sql)
        total_amount += int(value)
        if not result:
            raise OperationalError("Dish is not appended")
    if role == 'client':
        _sql = sql_provider.get('update_order.sql', dict(order_id=order_id, prepaid_expense=price,
                                                         dish_amount=total_amount, order_status="Полностью оформлен"))
    else:
        _sql = sql_provider.get('manager_update_order.sql', dict(order_id=order_id, add_pay=price,
                                                                 add_amount=total_amount,
                                                                 order_status="Ждет оплаты"))
    res = update(db_config, _sql)
    if not res:
        raise OperationalError("Order list is not updated")

    result = tuple(str(order_id))
    return ProductInfoRespronse(result, error_message="", status=True)
