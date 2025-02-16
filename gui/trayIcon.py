import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget, QCheckBox, QSystemTrayIcon, \
    QMenu, QAction, qApp
from PyQt5.QtCore import QSize

from named_tuple import msgConnect


class MainWindow(QMainWindow):
    """
        Объявление чекбокса и иконки системного трея.
        Инициализироваться будут в конструкторе.
    """
    # check_box = None
    tray_icon = None
    is_show = False
    queue = None

    # Переопределяем конструктор класса
    def __init__(self, queue):
        # Обязательно нужно вызвать метод супер класса
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
        # self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))

        if msg[0].status: # todo rework
            self.tray_icon.setIcon(QIcon("icon\cashRegister.png"))
        else:
            self.tray_icon.setIcon(QIcon("icon\cashRegisterBW.png"))

        show_action = QAction("Настройки", self)
        quit_action = QAction("Выход", self)
        # hide_action = QAction("Скрыть", self)
        show_action.triggered.connect(self.show)
        # hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        # tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.double_click)

    def double_click(self, event):
        if event == QSystemTrayIcon.DoubleClick:
            if self.is_show:
                self.hide()
            else:
                # self.tray_icon.showMessage(f"{self.queue.get()}", QSystemTrayIcon.Information, 2000)
                self.show()
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
    mw = MainWindow(queue)
    # mw.queue = queue

    # системный выход с кодом, который вернет app.exec()
    sys.exit(app.exec())
