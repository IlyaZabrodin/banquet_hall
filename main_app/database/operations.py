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


def call_procedure(db_config: dict, proc_name: str, *args):
    """
    Выполняет вызов процедур.

    Args:
        db_config: dict - Конфиг для подключения к БД.
        proc_name: dict - название процедуры.
        *args: str - параметры процедуры.
    Return:
        Флаг-значение вызова процедуры, в зависимости от успешности ее выполнения.
    """

    provider = SQLProvider(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'sql'))

    res = []
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('')
        param_list = []
        for arg in args:
            param_list.append(arg)

        if param_list[0] == 1:
            call_statement = provider.get(
                'call_worker_procedure.sql',
                {'month': param_list[1],
                 'year': param_list[2]}
            )
        elif param_list[0] == 0:
            call_statement = provider.get(
                'call_sale_procedure.sql',
                {'month': param_list[1],
                 'year': param_list[2]}
            )
        cursor.execute(call_statement)
        res = cursor.fetchone()[0]
    return res
