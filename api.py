import sys

from flask import Flask
from atol import Atol

flaskApp = Flask(__name__)

address = 'http://127.0.0.1:5000'

def flaskRoutes():
    @flaskApp.route('/')
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
                f'<div><a href="{address}/jsonCmd">open session</a></div>'
                f'<div><a href="{address}/getFnInfo">getFnInfo</a></div>'
                )

    @flaskApp.route('/model')
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

    @flaskApp.route('/jsonCmd')
    def json_cmd():
        atol = Atol()
        result = atol.jsonCmd({"type": "openShift"})
        atol.close()
        return result

    @flaskApp.route('/getFnInfo')
    def get_fn_status():
        atol = Atol()
        result = atol.getFnInfo({"type": "getFnInfo"})
        atol.close()
        return result


def flask_start():
    flaskRoutes()
    flaskApp.run()
    # sys.exit(flaskApp.run(debug=True))



