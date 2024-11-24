import os
from base64 import b64decode
from flask import Blueprint, current_app, request, jsonify

from database.sql_provider import SQLProvider
from database.operations import select_dict


blueprint_auth = Blueprint('blueprint_auth', __name__)
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


def valid_authorization_request(api_request):
    auth_header = api_request.headers.get('Authorization', '')
    if not auth_header:
        return False
    if not auth_header.startswith('Basic '):
        return False
    if len(auth_header) <= len('Basic '):
        return False
    return True


def decode_basic_authorization(api_request):
    auth_header = api_request.headers.get('Authorization')
    token = auth_header.split()[-1]
    login_and_password = b64decode(token.encode('ascii')).decode('ascii').split(':')
    if len(login_and_password) != 2:
        raise ValueError('Invalid login and password format')
    login, password = login_and_password
    return login, password


@blueprint_auth.route('/find-user', methods=['GET'])
def find_user():
    if not valid_authorization_request(request):
        return jsonify({'status': 400, 'message': 'Bad request'})

    try:
        login, password = decode_basic_authorization(request)
    except Exception as e:
        return jsonify({'status': 400, 'message': f'Bad request. {str(e)}'})
    else:
        sql = provider.get('find_external_user.sql', dict(login=login, password=password))
        user = select_dict(current_app.config['db_config'], sql)
        if not user:
            return jsonify({'status': 404, 'message': 'user not found'})
        print(user)
        print(user[0]['user_id'], user[0]['user_group'])
        return jsonify({'status': 200, 'message': 'OK', 'user_id': user[0]['user_id'], 'user_group': user[0]['user_group']})
