import time
from atol import Atol
from gui.trayIcon import qt_start
from api import flask_start
from multiprocessing import Process, Queue

def getAtolInfo():
    atol = Atol()
    try:
        if atol.init():
            return atol.info()
        else:
            return None
    except Exception:
        print(f'Error {Exception}')
        return None
    finally:
        atol.close()

if __name__ == '__main__':
    # очередь для обмена сообщениями между process Flask и process GUI Qt
    queue = Queue()

    process_flask = Process(target=flask_start, args=([queue]), daemon=True)
    process_flask.start()

    process_qt = Process(target=qt_start, args=([queue]), daemon=True)
    process_qt.start()

    # периодический опрос состояния Атол и отправка в GUI для отображения
    # while True:
    #     atolInfo = getAtolInfo()
    #     if atolInfo:
    #         queue.put(atolInfo)
    #     time.sleep(5)
