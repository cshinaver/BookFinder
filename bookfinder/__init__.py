from flask import Flask

app = Flask(__name__)

import bookfinder.views  # noqa
import bookfinder.search  # noqa
import bookfinder.api  # noqa
