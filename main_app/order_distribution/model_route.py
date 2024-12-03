from database.operations import select
from database.connection import DBContextManager


def model_route(sql_provider, context: dict):

    if context['action'] == 'GET':
        _sql = sql_provider.get('search_managers.sql', dict(order_date=context["order_time"]))
        result, schema = select(context['db_config'], _sql)
        render_data = {
            'status': True if result else False,
            'data': [i for i in result]
        }
        return render_data
    else:
        _sql = sql_provider.get(
            'set_manager.sql',
            {'manager_id': context['manager_id'],
             'order_id': context['order_id'],
             'order_status': context['order_status']}
        )
        with DBContextManager(context['db_config']) as cursor:
            cursor.execute(_sql)
