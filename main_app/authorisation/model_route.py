from base64 import b64encode
import requests
from flask import request, session, redirect, url_for, render_template
from database.operations import select_dict


def create_basic_auth_token(login, password):
    credentials_b64 = b64encode(f'{login}:{password}'.encode('ascii')).decode('ascii')
    token = f'Basic {credentials_b64}'
    return token


def save_in_session_and_redirect(user_dict):
    session['user_id'] = user_dict['user_id']
    session['user_group'] = user_dict['user_group']
    session.permanent = True
    print(1)
    return redirect(url_for('menu_choice'))


def model_route(db_config: dict, sql_provider, request):
    login = request.form.get('login', '')
    password = request.form.get('password', '')
    is_internal = True if request.form.get('is_internal') == 'on' else False
    print(login, password)

    if not is_internal:
        # make external API call
        response = requests.get(
            f'http://127.0.0.1:5002/api/authorisation/find-user',
            headers={'Authorization': create_basic_auth_token(login, password)}
        )

        resp_json = response.json()
        if resp_json['status'] == 200:
            return save_in_session_and_redirect(resp_json)
    else:
        # find internal user
        sql = sql_provider.get('find_internal_user.sql', dict(login=login, password=password))
        user = select_dict(db_config, sql)
        if user:
            return save_in_session_and_redirect(user[0])
    return render_template('input_login.html', message='Пользователь не найден')
