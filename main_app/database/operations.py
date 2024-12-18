from flask import current_app
from pymysql.err import OperationalError
from database.connection import DBContextManager


def select(db_config, sql):
    """
    Выполняет запрос (SELECT) к БД с указанным конфигом и запросом.

    Args:
        db_config: dict - Конфиг для подключения к БД.
        sql: str - SQL-запрос.
    Return:
        Кортеж с результатом запроса и описанием колонок запроса.
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
    procedures = current_app.config["procedures"]["procedure_name"]

    res = []
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('')
        param_list = []
        for arg in args:
            param_list.append(arg)

        cursor.callproc(procedures[param_list[0]], (param_list[1], param_list[2]))

        res = cursor.fetchone()[0]
    return res


def update(db_config: dict, _sql: str):
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError("Cursor not created")
        else:
            try:
                cursor.execute(_sql)
            except OperationalError as error:
                print("error: ", error)
                return False

    return True


def delete(db_config: dict, _sql: str):
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError("Cursor not created")
        else:
            try:
                cursor.execute(_sql)
            except OperationalError as error:
                print("error: ", error)
                return False

    return True
