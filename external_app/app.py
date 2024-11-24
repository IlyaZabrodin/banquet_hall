import json
from pathlib import Path

from flask import Flask

from authorisation.routes import blueprint_auth


app = Flask(__name__)

project_path = Path(__file__).resolve().parent
app.config['db_config'] = json.load(open(project_path / 'configs/db.json'))

app.register_blueprint(blueprint_auth, url_prefix='/api/authorisation')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002)
