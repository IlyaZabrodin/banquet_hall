import os
from flask import Blueprint, render_template, request, session, redirect, current_app

from database.sql_provider import SQLProvider
from access import login_required
from query_execution.model_route import model_route

from main_app.query_execution.model_route import model_route

query_blueprint = Blueprint(
    'bp_query',
    __name__,
    template_folder='templates'
)

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@query_blueprint.route('/', methods=['GET', 'POST'])
@login_required(['hall_admin', 'client', 'manager'])
def form_render():
    if request.method == 'GET':
        if session.get('user_group') in ['hall_admin']:

            if request.args.get('query_code', default=None, type=int) == 3:
                render_data, min_date, max_date = model_route(provider, current_app.config['db_config'], request)
                return render_template('query_form_for_admin.html', query_code=session["query_code"],
                                       min_date=min_date, max_date=max_date, render_data=render_data)

            render_data, indexes = model_route(provider, current_app.config['db_config'], request)
            return render_template('query_form_for_admin.html', query_code=session["query_code"],
                                   render_data=render_data, indexes=indexes)
        else:
            render_data, st_code = model_route(provider, current_app.config['db_config'], request)
            return render_template(
                'query_out.html',
                render_data=render_data,
                status_code=st_code
            )
    elif request.method == 'POST':
        render_data, empty_code = model_route(provider, current_app.config['db_config'], request)
        if request.args.get('query_code', default=None, type=int) == 2:
            obj = session['manager_choice']
        else:
            obj = session['hall_choice']

        return render_template(
            'query_out.html',
            render_data=render_data,
            status_code=1,
            query_code=session["query_code"],
            empty_code=empty_code,
            obj=obj
        )
