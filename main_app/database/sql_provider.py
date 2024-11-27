import os
from string import Template


class SQLProvider:
    """Класс, для получения SQL-запроса по его названию."""

    def __init__(self, file_path: str) -> None:
        """
        Инициализация.

        Args:
             file_path: str - Путь до папки с шаблонами SQL-запросы.
        """

        self._scripts: dict[str, Template] = {}
        for file in os.listdir(file_path):
            self._scripts[file] = Template(open(f'{file_path}/{file}').read())

    def get(self, name: str, kwargs: dict = None) -> str:
        """
        Выдает SQL-запрос по его названию.

        Args:
            name: str - Название запроса.
            kwargs: dict - Аргументы запроса.
        Returns:
            str - SQL-запрос
        """

        if name not in self._scripts:
            raise ValueError(f'No such sql-script: {name}')

        kwargs = kwargs or {}

        return self._scripts.get(name).substitute(**kwargs)
