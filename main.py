from gui.trayIcon import qt_start
from api import flask_start
from multiprocessing import Process, Queue

if __name__ == '__main__':
    # очередь для обмена сообщениями между process Flask и GUI Qt
    queue = Queue()
    process_flask = Process(target=flask_start, args=([queue]), daemon=True)
    process_flask.start()

    qt_start(queue)
