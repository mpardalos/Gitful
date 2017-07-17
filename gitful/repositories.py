import json
from collections import namedtuple

import git
from pathlib import Path

from .exceptions import RepoNotFound
from . import app

repos_dir = Path(app.config['REPOS_DIR'])

class Repository():
    @classmethod
    def from_id(cls, id):
        self = cls()
        self.path = repos_dir/str(id)
        if not self.path.exists():
            raise RepoNotFound()

        try:
            with open(self.path / 'gitful_conf.json') as f:
                self._conf = json.load(f)
        # If the folder exists but does not have a config, act as if the repo does not exist
        except FileNotFoundError:
            raise RepoNotFound()

        self._repo = git.Repo(self.path)
        self.id = id

        return self


    @classmethod
    def all(cls):
        for repo_dir in repos_dir.iterdir():
            yield Repository.from_id(repo_dir.name)

    @property
    def name(self):
        return self._conf['name']

