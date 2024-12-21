from flask import Flask
from jinja2.runtime import exported

app = Flask(__name__)

def routes():
    @app.route('/init')
    def init():
        return 'Hello world'

    @app.route('/jsonCmd')
    def jsonCmd():
            return 'JsonCmd'


def start(self):
    self.routes()
    self.app.run(debug=True)

