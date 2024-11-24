from database.connection import DBContextManager


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
