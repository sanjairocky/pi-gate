from flask import Flask, render_template
from flask_sock import Sock
import platform
import socket

app = Flask(__name__)
sock = Sock(app)


@app.route('/')
def index():
    return render_template('index.html')


@sock.route('/echo')
def echo(sock):
    while True:
        data = sock.receive()
        sock.send(data)

if platform.uname().system.lower()=='linux':
    print("Detected Linux, Preparing gunicorn")        
    import gunicorn.app.base
    class StandaloneApplication(gunicorn.app.base.BaseApplication):

        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super().__init__()

        def load_config(self):
            config = {key: value for key, value in self.options.items()
                    if key in self.cfg.settings and value is not None}
            for key, value in config.items():
                self.cfg.set(key.lower(), value)

        def load(self):
            return self.application

if __name__ == "__main__":
    # Use a debugging session in port 5001    
    if platform.uname().system.lower()=='linux':
        print("Detected Linux, Running Gunicorn")
        options = {
            'bind': '%s:%s' % ('0.0.0.0', '5001'),
            'workers': 1,
            # 'threads': number_of_workers(),
            'timeout': 120,
        }
        StandaloneApplication(app, options).run()
    else:
        print("Detected non Linux, Running in pure Flask")
        app.run(debug=True, host=socket.gethostbyname(socket.gethostname()), port=5001)