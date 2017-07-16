import sys

import os
from flask import Flask
from flask_restful import Api

app = Flask(__name__)

if 'dev' in sys.argv:
    app.config.update(
        DEBUG=True,
        SECRET_KEY='DevKey',
        REPOS_DIR='test_repos'
    )

if not os.path.exists(app.config['REPOS_DIR']):
    os.mkdir(app.config['REPOS_DIR'])

api = Api(app)

from . import endpoints

