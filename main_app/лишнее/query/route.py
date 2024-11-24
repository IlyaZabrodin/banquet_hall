from flask import Blueprint

from access import login_required


query_blueprint = Blueprint('bp_query', __name__, template_folder='templates')


@query_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def queries():
    return 'Hello from query'
