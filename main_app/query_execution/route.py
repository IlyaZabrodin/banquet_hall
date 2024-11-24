import os
from flask import Blueprint, render_template, request, session, redirect, current_app

from database.sql_provider import SQLProvider
from database.connection import DBContextManager
from access import login_required

query_blueprint = Blueprint(
    'bp_query',
    __name__,
    template_folder='templates'
)

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@query_blueprint.route('/', methods=['GET', 'POST'])
@login_required(['manager', 'hall_admin', 'admin'])
def form_render():
    if request.method == 'GET':
        return render_template('query_form.html')
    elif request.method == 'POST':
        prod_category = request.form.get('product-category', '')
        sql_statement = provider.get(
            'find_product_category.sql',
            {'prod_category': prod_category}
        )

        render_data = find_product_by_category(current_app.config['db_config'], sql_statement)

        return render_template(
            'query_out.html',
            render_data=render_data
        )


def find_product_by_category(db_conf, sql):
    with DBContextManager(db_conf) as cursor:
        cursor.execute(sql)
        schema = [column[0] for column in cursor.description]
        result = [dict(zip(schema, row)) for row in cursor.fetchall()]

    render_data = {
        'status': True if result else False,
        'data': result
    }
    return render_data
