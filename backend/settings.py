# TODO review

DEBUG = None
APP_PORT = None
FLASK_APP = None
FLASK_ENV = None
SECRET_KEY = None
DATABASE_URL = None


try:
    # load settings from `local_settings.py`
    from local_settings import *
except ImportError as exc:
    pass
