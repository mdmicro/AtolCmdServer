from libs.libfptr10 import IFptr

fptr = IFptr()

class Atol:
    def __init__(self):
        fptr.open()

    def jsonCmd(self, cmd):
        try:
            fptr.setParam(IFptr.LIBFPTR_PARAM_JSON_DATA, cmd)
            fptr.validateJson()
            fptr.processJson()
            result = fptr.getParamString(IFptr.LIBFPTR_PARAM_JSON_DATA)
            return result
        except:
            return 'Error'

