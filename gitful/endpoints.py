from flask import jsonify
from flask_restful import Resource

from . import app
from .repositories import Repository, RepoNotFound

@app.route('/repos', methods=['GET'])
def get_all_repos():
    pass

@app.route('/repos', methods=['POST'])
def create_repo():
    pass

@app.route('/repos/<int:repo_id>', methods=['GET'])
def get_repo(repo_id):
    try:
        repo = Repository(repo_id)
    except RepoNotFound:
        return jsonify({
            'error': 'no repository with that id exists'
        }), 404
    else:
        return jsonify({
            "id": repo.id,
            "name": repo.name
        })


