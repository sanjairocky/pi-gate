from flask import Blueprint, redirect
from .git import git_api
from .ci import ci_api

api = Blueprint('root', __name__, url_prefix='/')


@api.get('/')
def index():
    return redirect("/ci", code=302)


api.register_blueprint(git_api)
api.register_blueprint(ci_api)
