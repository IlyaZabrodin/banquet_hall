import os
import json
from pathlib import Path
from flask import Flask, render_template, request, session, redirect, current_app

from database.sql_provider import SQLProvider
from database.operations import select

from authorisation.route import auth_blueprint
from query_execution.route import query_blueprint
from report.routes import blueprint_report
from order_making.route import blueprint_order_make
from access import login_required

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


class Properties:

    def __init__(self, user_id: int, role: str) -> None:
        self.role = role
        self.id = user_id
        if self.role == "client":
            self.show_client()
        elif self.role == "manager":
            self.show_manager()
        elif self.role == "director":
            self.show_director()
        elif self.role == "hall_admin":
            self.show_hall_admin()

    def show_client(self):
        sql = provider.get('find_order.sql', dict(user_id=self.id))
        result, schema = select(current_app.config['db_config'], sql)
        render_data = {
            'status': True if result else False,
            'data': [i for i in result]
        }
        return render_template('external_user_menu.html', render_data=render_data)

    def show_manager(self):
        pass

    def show_director(self):
        pass

    def show_hall_admin(self):
        pass
