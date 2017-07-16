from flask import jsonify
from flask_restful import Resource

from . import app

@app.route('/repos', methods=['GET'])
def get_all_repos():
    pass

@app.route('/repos', methods=['POST'])
def create_repo():
    pass

@app.route('/repos/<int:repo_id>', methods=['GET'])
def get_repo(repo_id):
    pass


