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
        model = atol.getModel()
        fn_info = atol.getFnInfo()

        atol.close()
        return (f'<div>Atol Web Server started</div> '
                f'<div>version: {res.version}</div>'
                f'<div>opened: {res.isOpened}</div>'
                f'<div><p>{res.settings}</p></div>'
                '</br>'
                f'<div><a href="{address}/init">init</a></div>'
                f'<div>model KKT: {model.name}</div>'
                f'<div>fnInfo: {fn_info}</div>'
                )

    # Инициализация драйвера, возвращает статус подключения к ККТ
    @flaskApp.route('/init')
    def init():
        try:
            atol = Atol()
            res = 'Ok' if atol.init() else 'Not connection'
            atol.close()
            return res
        except Exception:
            return f'Error {Exception}'

    @flaskApp.route('/jsonCmd')
    def json_cmd():
        atol = Atol()
        result = atol.jsonCmd({"type": "openShift"})
        atol.close()
        return result

def flask_start():
    flaskRoutes()
    sys.exit(flaskApp.run())



