import os
from flask import Blueprint, current_app, request, jsonify

from database.sql_provider import SQLProvider
from authorisation.model_route import model_route, valid_authorization_request


blueprint_auth = Blueprint('blueprint_auth', __name__)
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_auth.route('/find-user', methods=['GET'])
def find_user():
    if not valid_authorization_request(request):
        return jsonify({'status': 400, 'message': 'Bad request'})
    return model_route(current_app.config['db_config'], provider, request)
