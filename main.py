from gui.trayIcon import qt_start
from api import flask_start
from multiprocessing import Process

if __name__ == '__main__':
    process_flask = Process(target=flask_start, daemon=True)
    process_flask.start()

    qt_start()

