import shutil

from flask import jsonify, request, url_for
from werkzeug.exceptions import BadRequest

from . import api
from .exceptions import InvalidRequest
from .repositories import Repository


@api.route('/repos', methods=['GET'])
def get_all_repos():
    return jsonify([
        {
            "id": repo.id,
            "name": repo.name
        }
        for repo in Repository.all()
    ])


@api.route('/repos', methods=['POST'])
def create_repo():
    try:
        args = request.json
    except BadRequest:
        raise InvalidRequest(message="Your request must contain a json body")

    if "name" not in args:
        raise InvalidRequest(message="Your request must contain a name field")

    repo = Repository(args['name'])

    return jsonify({
        "id": repo.id,
        "url": url_for('api.get_repo', repo_id=repo.id)
    })


@api.route('/repos/<int:repo_id>', methods=['GET'])
def get_repo(repo_id):
    repo = Repository.from_id(repo_id)
    return jsonify({
        "id": repo.id,
        "name": repo.name
    })


@api.route('/repos/<int:repo_id>', methods=['DELETE'])
def delete_repo(repo_id):
    Repository.from_id(repo_id).destroy()
    return '', 200


