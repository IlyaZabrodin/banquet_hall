import os
from database.connection import DBContextManager
from database.sql_provider import SQLProvider


def select(db_config, sql):
    """
    Выполняет запрос (SELECT) к БД с указанным конфигом и запросом.

    Args:
        db_config: dict - Конфиг для подключения к БД.
        sql: str - SQL-запрос.
    Return:
        Кортеж с результатом запроса и описанеим колонок запроса.
    """

    result = []
    schema = []

    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('Cursor not found')

        cursor.execute(sql)
        schema = [column[0] for column in cursor.description]
        result = cursor.fetchall()

    return result, schema


def select_dict(db_config, sql):
    """
    Выполняет запрос (SELECT) к БД с указанным конфигом и запросом.

    Args:
        db_config: dict - Конфиг для подключения к БД.
        sql: str - SQL-запрос.
    Return:
        Список словарей, где словарь это строка результата sql-запроса.
    """

    rows, schema = select(db_config, sql)
    return [dict(zip(schema, row)) for row in rows]


def call_proc(db_config: dict, proc_name: str, *args):
    provider = SQLProvider(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'sql'))

    res = []
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('')
        param_list = []
        for arg in args:
            param_list.append(arg)
        print()
        print(f"param_list = {param_list}")
        print(f"proc_name = {proc_name}")
        print()
        call_statement = provider.get(
            'call_procedure.sql',
            {'param_list0': param_list[0],
             'param_list1': param_list[1]}
        )
        print(call_statement)
        cursor.execute(call_statement)
        res = cursor.fetchone()[0]
        print()
        print(f"cursor.callproc = {res}")
        print()
    return res
