import json
import time
from collections import namedtuple
from libs.libfptr10 import IFptr


class Atol:
    def __init__(self):
        self.fptr = IFptr()

    def connect(self):
        for i in range(10):
            if self.fptr.isOpened():
                return True
            # time.sleep(1)
            self.fptr.open()
        return False

    def close(self):
        self.fptr.close()

    # {uuid, request }
    def jsonCmd(self, data, uuid = None):
        error = ''
        try:
            cmd = json.dumps(data)

            self.fptr.setParam(IFptr.LIBFPTR_PARAM_JSON_DATA, cmd)
            self.fptr.validateJson()
            self.fptr.setParam(IFptr.LIBFPTR_PARAM_JSON_DATA, cmd)
            self.fptr.processJson()

            response = self.fptr.getParamString(IFptr.LIBFPTR_PARAM_JSON_DATA)
            return JsonCmdResponse(data = response, uuid = uuid, error = error)
        except Exception:
            return JsonCmdResponse('', '',Exception)

    def getFnInfo(self):
        req = {"type": "getFnInfo"}
        data = {'request': req, 'uuid': None}
        res = self.jsonCmd(data)
        return json.load(res.data) if res.data else None

    def info(self):
        version = self.fptr.version()
        isOpened = self.fptr.isOpened()
        settings = self.fptr.getSettings()
        return InfoCmdResponse(version, isOpened, settings)

    def getModel(self):
        self.fptr.setParam(IFptr.LIBFPTR_PARAM_DATA_TYPE, IFptr.LIBFPTR_DT_MODEL_INFO)
        self.fptr.queryData()

        model = self.fptr.getParamInt(IFptr.LIBFPTR_PARAM_MODEL)
        name = self.fptr.getParamString(IFptr.LIBFPTR_PARAM_MODEL_NAME)
        firmwareVersion = self.fptr.getParamString(IFptr.LIBFPTR_PARAM_UNIT_VERSION)

        return ModelResponse(model, name, firmwareVersion)

    def init(self):
        if self.fptr.isOpened():
            return True
        else:
            settings = self.fptr.getSettings()
            self.fptr.setSettings(settings)
            # time.sleep(1)
            # self.fptr.setSingleSetting(IFptr.LIBFPTR_SETTING_PORT, str(IFptr.LIBFPTR_PORT_COM))
            # self.fptr.setSingleSetting(IFptr.LIBFPTR_SETTING_COM_FILE, str(5))
            # self.fptr.applySingleSettings()
            # self.fptr.initDevice()
            # fptr.showProperties()
            return self.connect()

JsonCmdResponse = namedtuple('JsonCmdResponse', ['data', 'uuid', 'error'])
InfoCmdResponse = namedtuple('InfoCmdResponse', ['version', 'isOpened', 'settings'])
ModelResponse = namedtuple('ModelResponse', ['model', 'name', 'firmwareVersion'])
