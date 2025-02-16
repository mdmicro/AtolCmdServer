import time
from atol import Atol
from gui.trayIcon import qt_start
from api import flask_start
from multiprocessing import Process, Queue

def getAtolInfo():
    atol = Atol()
    try:
        resInit = atol.init()

        if resInit:
            return atol.info()
        else:
            return None
    except Exception:
        print(f'Error {Exception}')
        return None
    finally:
        atol.close()

if __name__ == '__main__':
    # очередь для обмена сообщениями между process Flask и GUI Qt
    queue = Queue()

    process_flask = Process(target=flask_start, args=([queue]), daemon=True)
    process_flask.start()

    process_qt = Process(target=qt_start, args=([queue]), daemon=True)
    process_qt.start()

    # опрос состояния Атол и отправка в очередь сообщений для gui
    while True:
        atolInfo = getAtolInfo()
        if atolInfo:
            queue.put(atolInfo)
        time.sleep(5)
