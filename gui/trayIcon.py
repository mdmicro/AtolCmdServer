import sys
import threading
import queue
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget, QCheckBox, QSystemTrayIcon, \
    QMenu, QAction, qApp, QPushButton
from PyQt5.QtCore import QSize
from atol import Atol, InfoCmdResponse

class MainWindow(QMainWindow):
    tray_icon = None
    is_show = False
    queue = None
    atol_info: InfoCmdResponse = None

    def get_msg_thread(self):
        while True:
            try:
                self.atol_info  = self.queue.get(block=True, timeout=10)
                if self.atol_info:
                    self.tray_icon.setIcon(QIcon("icon\cashRegister.png"))

            except queue.Empty:
                self.tray_icon.setIcon(QIcon("icon\cashRegisterBW.png"))
                continue

    def __init__(self, queue):
        QMainWindow.__init__(self)

        # Инициализируем QSystemTrayIcon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("icon\cashRegisterBW.png"))

        show_action = QAction("Настройки", self)
        quit_action = QAction("Выход", self)

        # обработчик события - показать окно формы
        show_action.triggered.connect(self.event_handler_show)
        quit_action.triggered.connect(qApp.quit)

        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.double_click)

        self.queue = queue
        thread = threading.Thread(target=self.get_msg_thread)
        thread.start()

    def event_handler_show(self):
        self.setMinimumSize(QSize(800, 180))  # Устанавливаем размеры
        self.setWindowTitle("Статус")  # Устанавливаем заголовок окна
        central_widget = QWidget(self)  # Создаём центральный виджет
        self.setCentralWidget(central_widget)  # Устанавливаем центральный виджет

        grid_layout = QGridLayout(self)  # Создаём QGridLayout
        central_widget.setLayout(grid_layout)  # Устанавливаем данное размещение в центральный виджет
        if self.atol_info:
            self.setMinimumSize(QSize(800, 480))  # Устанавливаем размеры
            grid_layout.addWidget(QLabel(f"Версия ДТО: {self.atol_info.version.decode('utf-8')}", self), 0, 0)
            grid_layout.addWidget(QLabel(f"Установки:", self), 2, 0)

            settings = self.atol_info.settings
            for index, (key, value) in enumerate(settings.items()):
                grid_layout.addWidget(QLabel(f"{key}: {value}", self), 3 + index, 0)

        self.show()

    def double_click(self, event):
        if event == QSystemTrayIcon.DoubleClick:
            if self.is_show:
                self.hide()
            else:
                self.event_handler_show()
            self.is_show = not self.is_show

    # Переопределение метода closeEvent, для перехвата события закрытия окна
    def closeEvent(self, event):
            event.ignore()
            self.hide()
            self.is_show = False

def qt_start(queue):
    app = QApplication(sys.argv)
    MainWindow(queue)

    # системный выход с кодом, который вернет app.exec()
    sys.exit(app.exec())
