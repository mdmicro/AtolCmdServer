from flask import Flask
from atol import Atol

app = Flask(__name__)

address = 'http://127.0.0.1:5000'

def routes():
    @app.route('/')
    def default():
        atol = Atol()
        res = atol.info()
        atol.close()
        return (f'<div>Atol Web Server started</div> '
                f'<div>version: {res.version}</div>'
                f'<div>opened: {res.isOpened}</div>'
                f'<div><p>{res.settings}</p></div>'
                '</br>'
                f'<div><a href="{address}/init">init</a></div>'
                f'<div><a href="{address}/model">model KKT</a></div>'
                f'<div><a href="{address}/jsonCmd">json cmd</a></div>'
                )

    @app.route('/model')
    def model():
        atol = Atol()
        model = atol.getModel()
        atol.close()

        return (f'<div>Atol Web Server</div>'
                f'<div>model: {model.model}</div>'
                f'<div>modelName: {model.name}</div>'
                f'<div>firmwareVersion: {model.firmwareVersion}</div>'
                )

    # @app.route('/init')
    # def init():
    #     try:
    #         return 'Ok' if atol.init() else 'Not connection'
    #     except:
    #         return 'Error'

    @app.route('/jsonCmd')
    def jsonCmd():
        atol = Atol()
        result = atol.jsonCmd({"type": "openShift"})
        atol.close()
        return result


def start():
    routes()
    app.run(debug=True)



