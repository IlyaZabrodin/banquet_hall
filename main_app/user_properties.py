import os
from flask import render_template, current_app

from database.sql_provider import SQLProvider
from database.operations import select

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


class Properties:

    def __init__(self, user_id: int, role: str) -> None:
        self.id = user_id
        self.role = role
        self.problem_orders = []
        # Словарь для обработки ролей
        self.role_configs = {
            'client': {
                'sql_file': 'find_order.sql',
                'template': 'external_user_menu.html',
                'params': {'user_id': self.id}
            },
            'manager': {
                'sql_file': 'find_manager_order.sql',
                'template': 'internal_user_menu_for_manager.html',
                'params': {'user_id': self.id, 'avoid_status': "Завершен"}
            },
            'director': {
                'sql_file': None,
                'template': 'internal_user_menu_for_director.html',
                'params': {}
            },
            'hall_admin': {
                'sql_file': 'find_not_processed_orders.sql',
                'template': 'internal_user_menu_for_hall_admin.html',
                'params': {'order_status': 'В обработке'}
            }
        }

    def show_template(self):
        # Проверка наличия конфигурации для роли
        if self.role not in self.role_configs:
            raise ValueError(f"Role {self.role} is not supported")

        user_props = self.role_configs[self.role]
        sql_file, template, params = user_props['sql_file'], user_props['template'], user_props['params']

        result, schema = ([], None)
        if sql_file:
            sql = provider.get(sql_file, params)
            result, schema = select(current_app.config['db_config'], sql)

        res = [i for i in result]
        # удобный просмотр заказов для клиентов
        if self.role == 'client':
            res = sorted(res, key=lambda i: i[0], reverse=True)

            # необходимое решение проблемы прерывания перехода от корзины к предоплате
            _sql = provider.get('find_problem_orders.sql', {'ord_stat': 'Подтвержден'})
            r, s = select(current_app.config['db_config'], _sql)
            self.problem_orders = [i[0] for i in r]

        render_data = {
            'status': True if result else False,
            'data': res
        }
        return render_template(template, render_data=render_data, problem_orders=self.problem_orders)
