import os

from flask import Flask

app = Flask(__name__)

# Config
# BOOKFINDER_SETTINGS must be set to development or production
settings_type = os.environ['BOOKFINDER_SETTINGS']

if settings_type == "development":
    app.config.from_object('bookfinder.settings.DevelopmentConfig')
elif settings_type == "production":
    app.config.from_object('bookfinder.settings.ProductionConfig')

import bookfinder.views  # noqa
