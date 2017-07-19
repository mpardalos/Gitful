import json
import os
import shutil
from pathlib import Path

import git

from . import app
from .exceptions import RepoNotFound

repos_dir = Path(app.config['REPOS_DIR'])


class Repository:
    def __init__(self, name):
        """
        Create a Repository backed by a brand new repo in REPOS_DIR

        Args:
            name: The name that will be given to the Repository
        """
        self.name = name

        # Give the repo the first available id
        with open(app.config['ID_FILE_PATH'], mode="r") as id_file:
            self.id = int(id_file.read())

        with open(app.config['ID_FILE_PATH'], mode="w") as id_file:
            id_file.write(str(self.id + 1))

        self.path = repos_dir / str(self.id)

        self._repo = git.Repo()
        self._repo.init(str(self.path), bare=True)  # Also creates the directory

        self._conf = {
            "name": self.name
        }
        with open(self.path / 'gitful_conf.json', 'x') as f:
            json.dump(self._conf, f)

    @classmethod
    def from_id(cls, repo_id):
        # Do not use __init__ because it creates brand new repos
        self = cls.__new__(cls)

        self.path = repos_dir / str(repo_id)
        if not self.path.exists():
            raise RepoNotFound()

        try:
            with open(self.path / 'gitful_conf.json') as f:
                self._conf = json.load(f)
        # If the folder exists but does not have a config, act as if the repo does not exist
        except FileNotFoundError:
            raise RepoNotFound()

        self.name = self._conf['name']

        self._repo = git.Repo(self.path)
        self.id = repo_id

        return self

    @classmethod
    def all(cls):
        for repo_dir in filter(os.path.isdir, repos_dir.iterdir()):
            yield Repository.from_id(repo_dir.name)

    def destroy(self):
        shutil.rmtree(str(self.path))
        del self

