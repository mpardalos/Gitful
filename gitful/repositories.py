import json
from collections import namedtuple

import git
from pathlib import Path

from . import app

repos_dir = Path(app.config['REPOS_DIR'])

class RepoNotFound(FileNotFoundError): pass

class ConfigNotFound(FileNotFoundError): pass

class Repository():
    def __init__(self, id):
        self.path = repos_dir/str(id)
        if not self.path.exists():
            raise RepoNotFound()

        try:
            with open(self.path / 'gitful_conf.json') as f:
                self._conf = json.load(f)
        except FileNotFoundError as e:
            raise ConfigNotFound(e)

        self._repo = git.Repo(self.path)
        self.id = id

    @classmethod
    def all(cls):
        for repo_dir in repos_dir.iterdir():
            yield Repository(repo_dir.name)

    @property
    def name(self):
        return self._conf['name']

