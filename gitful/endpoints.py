from flask_restful import Resource

from . import app, api

class Repositories(Resource):
    def get(self):
        pass

    def post(self):
        pass

class Repository(Resource):
    def get(self, repo_id):
        pass

