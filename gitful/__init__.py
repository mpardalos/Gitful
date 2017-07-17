import os
import sys
from pathlib import Path

from flask import Flask

app = Flask(__name__)

if 'dev' in sys.argv:
    app.config.update(
        DEBUG=True,
        SECRET_KEY='DevKey',
        REPOS_DIR='test_repos'
    )

# Contains the first available repo id. When a new repo is created, it gets the id contained in this file,
# which is then incremented
app.config['ID_FILE_PATH'] = Path(app.config['REPOS_DIR']) / '.gitful.json'
if not app.config['ID_FILE_PATH'].exists():
    with open(app.config['ID_FILE_PATH'], mode='x') as f:
        f.write("1")

if not os.path.exists(app.config['REPOS_DIR']):
    os.mkdir(app.config['REPOS_DIR'])

# noinspection PyPep8
from . import endpoints
