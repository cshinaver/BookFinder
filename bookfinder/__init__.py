from flask import Flask

app = Flask(__name__)

import bookfinder.views  # noqa
import bookfinder.search.views  # noqa
import bookfinder.search.prices.views  # noqa
import bookfinder.api.views  # noqa
