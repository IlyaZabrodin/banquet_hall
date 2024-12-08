from pymysql import connect
from pymysql.err import OperationalError


class DBContextManager:
    """Класс для подключения к БД и выполнения sql-запросов."""

    def __init__(self, config):
        """
        Инициализация объекта подключения.

        Args:
             config: dict - Конфиг дял подключения к БД.
        """
        self.config = config
        self.conn = None
        self.cursor = None

    def __enter__(self):
        """
        Реализует логику входа в контекстный менеджер.
        Создает соединение к БД и возвращает курсор для выполнения запросов.

        Return:
            Курсор для работы с БД или NULL.
        """
        try:
            self.conn = connect(**self.config)
            self.cursor = self.conn.cursor()
            return self.cursor

        except OperationalError as err:
            print(str(err))
            return None

    def __exit__(self, exc_type, exc_val, exc_tr):
        """
        Реализует логику выхода из контекстного менеджера для работы с БД.
        Закрывает соединение и курсор.
        Возвращаемое значение всего True для обеспечения сокрытия списка ошибок в консоли.

        Args:
            exc_type: Тип возможной ошибки при работе менеджера.
            exc_val: Значение возможной ошибки при работе менеджера.
            exc_tr: Traceback (подробный текст ошибки) при работе менеджера.
        """

        if self.conn and self.cursor:
            if exc_type:
                print('Invalid DB operation. Rollback')
                self.conn.rollback()
            else:
                self.conn.commit()
            self.conn.close()
            self.cursor.close()
        else:
            if exc_type:
                print('exc_type', exc_type)
                print('exc_val', exc_val)
        return True
