import time

from flask import Flask
from libs.libfptr10 import IFptr
import json

app = Flask(__name__)
fptr = IFptr()

def routes():
    @app.route('/')
    def default():
        fptr.open()
        isOpened = fptr.isOpened()
        return (f'<div>Atol Web Server started</div> <div>version: {fptr.version()}\n opened: {isOpened}</div>'
                f'<div><span>{fptr.getSettings()}</span></div>'
                f'<div></div>'
                )

    @app.route('/init')
    def init():
        return 'Hello world'

    @app.route('/jsonCmd')
    def jsonCmd():
            # processJson
            # validateJson
            return 'JsonCmd'


def start():
    routes()
    app.run(debug=True)
    settings = fptr.getSettings()
    # fptr.setSingleSetting(IFptr.LIBFPTR_SETTING_PORT, str(IFptr.LIBFPTR_PORT_USB))
    # fptr.applySingleSettings()
    fptr.setSettings(settings)
    # fptr.initDevice()
    # fptr.showProperties()
    # time.sleep(2)
    # fptr.open()


