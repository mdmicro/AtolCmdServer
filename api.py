import json
from flask import Flask
from flask_restful.fields import String
from libs.libfptr10 import IFptr
import time
from atol import Atol

app = Flask(__name__)
fptr = IFptr()
# atol = Atol()

address = 'http://127.0.0.1:5000'

def routes():
    @app.route('/')
    def default():
        return (f'<div>Atol Web Server started</div> '
                f'<div>version: {fptr.version()}</div>'
                f'<div>opened: {fptr.isOpened()}</div>'
                f'<div><p>{json.dumps(fptr.getSettings(), indent=4)}</p></div>'
                f'<div><a href="{address}/init">init</a></div>'
                f'<div><a href="{address}/model">model KKT</a></div>'
                f'<div><a href="{address}/jsonCmd">json cmd</a></div>'
                )

    @app.route('/model')
    def model():
        if fptr.isOpened():
            fptr.setParam(IFptr.LIBFPTR_PARAM_DATA_TYPE, IFptr.LIBFPTR_DT_MODEL_INFO)
            fptr.queryData()

            model = fptr.getParamInt(IFptr.LIBFPTR_PARAM_MODEL)
            modelName = fptr.getParamString(IFptr.LIBFPTR_PARAM_MODEL_NAME)
            firmwareVersion = fptr.getParamString(IFptr.LIBFPTR_PARAM_UNIT_VERSION)
            return (f'<div>Atol Web Server</div>'
                    f'<div>model: {model}</div>'
                    f'<div>modelName: {modelName}</div>'
                    f'<div>firmwareVersion: {firmwareVersion}</div>'
                    )
        else:
            return (f'<div>Atol Web Server</div>'
                    f'<div>KKT not connected</div>'
                    )

    @app.route('/init')
    def init():
        if fptr.isOpened():
            return 'ok'
        else:
            settings = fptr.getSettings()
            # fptr.setSingleSetting(IFptr.LIBFPTR_SETTING_PORT, str(IFptr.LIBFPTR_PORT_USB))
            # fptr.applySingleSettings()
            fptr.setSettings(settings)
            fptr.initDevice()
            # fptr.showProperties()
            time.sleep(2)
            fptr.open()
            return 'ok'


    @app.route('/jsonCmd')
    def jsonCmd():
        # result = atol.jsonCmd({"type": "openShift"})
        # return result
        pass


def start():
    routes()
    app.run(debug=True)



