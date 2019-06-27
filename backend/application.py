import settings

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import config
from api import configure_api
from database import db
from flask_cors import CORS


def create_app(config_name):
    app = Flask('api-pessoas-crud')
    app.config.from_object(config[config_name])

    db. init_app(app)
    configure_api(app)

    return app


app = create_app(settings.FLASK_ENV or 'default')
CORS(app, resources=r'/*')


if __name__ == '__main__':
    ip = 'localhost'
    port = app.config['APP_PORT']
    debug = app.config['DEBUG']

    app.run(
        host=ip, debug=debug, port=port, use_reloader=debug
    )
    db.create_all()
