from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
from gevent.pywsgi import WSGIServer
from utils.env import load_config, get_env_variable
import traceback
from routes import api
from service.BotService import BotService
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

app = Flask(__name__)


app.url_map.strict_slashes = False

bot = BotService()


@app.errorhandler(Exception)
def handle_error(e):
    traceback.print_exc()
    code = 500
    if isinstance(e, ValueError):
        code = 400
    elif isinstance(e, HTTPException):
        code = e.code
    elif isinstance(e, Exception):
        return jsonify(error="Internal Server Error"), code
    return jsonify(error=str(e)), code


app.register_blueprint(api)

if __name__ == "__main__":
    port = int(get_env_variable('PORT', '8080'))
    load_config()
    from utils.db import gen_session, current_e
    # from sqlalchemy import text
    # with gen_session() as con:
    #     with open("tables.sql") as file:
    #         for sql in file.read().split(';'):
    #             con.execute(text(sql))
    from models import BaseModel
    gen_session()
    BaseModel.metadata.create_all(bind=current_e[0])
    if get_env_variable("FLASK_ENV") == 'production':
        # Production
        http_server = WSGIServer(('', port), app)
        http_server.serve_forever()
    else:
        # Debug/Development
        app.run(debug=True, host='0.0.0.0', port=port)
