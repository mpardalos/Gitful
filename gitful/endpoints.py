from flask import jsonify, request, url_for
from werkzeug.exceptions import BadRequest

from . import app
from .exceptions import InvalidRequest
from .repositories import Repository


@app.route('/repos', methods=['GET'])
def get_all_repos():
    return jsonify([
        {
            "id": repo.id,
            "name": repo.name
        }
        for repo in Repository.all()
    ])


@app.route('/repos', methods=['POST'])
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
        "url": url_for('get_repo', repo_id=repo.id)
    })


@app.route('/repos/<int:repo_id>', methods=['GET'])
def get_repo(repo_id):
    repo = Repository.from_id(repo_id)
    return jsonify({
        "id": repo.id,
        "name": repo.name
    })
