from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea

from Rare.utils.legendary import get_installed
from Rare.GameWidget import GameWidget


class BrowserTab(QWebEngineView):
    def __init__(self, parent):
        super(BrowserTab, self).__init__(parent=parent)
        self.load(QUrl("https://www.epicgames.com/store/"))
        self.show()


class Settings(QWidget):
    def __init__(self, parent):
        super(Settings, self).__init__(parent=parent)
        self.layout = QVBoxLayout()
        label = QLabel()
        print(label.fontInfo().pixelSize())
        self.layout.addWidget(QLabel("<h1>Settings</h1>"))
        self.layout.addWidget(QLabel("Coming soon"))
        self.layout.addStretch(1)
        self.setLayout(self.layout)


class GameListInstalled(QScrollArea):
    def __init__(self, parent):
        super(GameListInstalled, self).__init__(parent=parent)
        self.widget = QWidget()
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.layout = QVBoxLayout()
        for i in get_installed():
            widget = GameWidget(i)
            #widget.setFixedSize(240, 340)
            self.layout.addWidget(widget)

        self.widget.setLayout(self.layout)
        self.setWidget(self.widget)


class GameListUninstalled(QScrollArea):
    def __init__(self, parent):
        super(GameListUninstalled, self).__init__(parent=parent)
        self.setWidget(QLabel("Hier kommen die nicht installierten Spiele"))


class UpdateList(QWidget):
    def __init__(self, parent):
        super(UpdateList, self).__init__(parent=parent)
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Updates"))
        self.setLayout(self.layout)
