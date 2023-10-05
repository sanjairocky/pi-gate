from flask import Blueprint
from .git import git_api

api = Blueprint('root', __name__, url_prefix='/')
    
@api.get('/')
def health_check():
    return "Api is up and running :)", 200

api.register_blueprint(git_api)
