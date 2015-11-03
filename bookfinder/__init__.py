import os

from flask import Flask
from flask.ext.login import LoginManager

app = Flask(__name__)

app.secret_key = 'super secret key'
# Config
# BOOKFINDER_SETTINGS must be set to development or production
settings_type = os.environ.get('BOOKFINDER_SETTINGS', None)

if settings_type == "development":
    app.config.from_object('bookfinder.settings.DevelopmentConfig')
elif settings_type == "production":
    app.config.from_object('bookfinder.settings.ProductionConfig')
elif not settings_type:
    app.config.from_object('bookfinder.settings.DevelopmentConfig')

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)


import bookfinder.views  # noqa
import bookfinder.purchase.views
import bookfinder.search.views  # noqa
import bookfinder.api.views  # noqa
import bookfinder.login.views  # noqa
