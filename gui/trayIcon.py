import json
import sys
import threading
from logging import exception
import queue
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget, QCheckBox, QSystemTrayIcon, \
    QMenu, QAction, qApp, QPushButton
from PyQt5.QtCore import QSize
from atol import Atol, InfoCmdResponse
from named_tuple import msgConnect

class MainWindow(QMainWindow):
    # check_box = None
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

        # Добавляем чекбокс, от которого будет зависеть поведение программы при закрытии окна
        # self.check_box = QCheckBox('Minimize to Tray')
        # grid_layout.addWidget(self.check_box, 1, 0)
        # grid_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding), 2, 0)

        # добавить Кнопку
        # btn = QPushButton('Обновить состояние',self)
        # btn.resize(btn.sizeHint())
        # btn.move(20,20)
        # btn.clicked.connect(self.on_click_update)

        # Инициализируем QSystemTrayIcon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("icon\cashRegisterBW.png"))

        show_action = QAction("Настройки", self)
        quit_action = QAction("Выход", self)
        # hide_action = QAction("Скрыть", self)

        # обработчик события - показать окно формы
        show_action.triggered.connect(self.event_handler_show)

        # hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        # tray_menu.addAction(hide_action)
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
            self.setMinimumSize(QSize(800, 580))  # Устанавливаем размеры
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
                # self.tray_icon.showMessage(f"{self.queue.get()}", QSystemTrayIcon.Information, 2000)
                self.event_handler_show()
            self.is_show = not self.is_show

    # Переопределение метода closeEvent, для перехвата события закрытия окна
    def closeEvent(self, event):
        # if self.check_box.isChecked():
            event.ignore()
            self.hide()
            self.is_show = False
            # self.tray_icon.showMessage("Tray Program", "Application was minimized to Tray", QSystemTrayIcon.Information, 2000)

def qt_start(queue):
    app = QApplication(sys.argv)
    MainWindow(queue)

    # системный выход с кодом, который вернет app.exec()
    sys.exit(app.exec())
