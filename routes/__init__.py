from flask import Blueprint
from .git import git_api
from .ci import ci_api

api = Blueprint('root', __name__, url_prefix='/')


@api.get('/')
def index():
    return "Api is up and running :)", 200


api.register_blueprint(git_api)
api.register_blueprint(ci_api)
