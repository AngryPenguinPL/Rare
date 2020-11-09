from logging import getLogger

from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QLineEdit, QPushButton

from Rare.GameWidget import GameWidget, UninstalledGameWidget
from Rare.utils.legendaryUtils import get_installed, get_not_installed, logout, get_updates, get_name

logger = getLogger("TabWidgets")


class BrowserTab(QWebEngineView):
    def __init__(self, parent):
        super(BrowserTab, self).__init__(parent=parent)
        self.load(QUrl("https://www.epicgames.com/store/"))
        self.show()


class Settings(QWidget):
    def __init__(self, parent):
        super(Settings, self).__init__(parent=parent)
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("<h1>Rare Settings</h1>"))
        self.logged_in_as = QLabel(f"Logged in as {get_name()}")
        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout)
        self.layout.addWidget(self.logged_in_as)
        self.layout.addWidget(self.logout_button)

        self.info_label = QLabel("<h2>Credits</h2>")
        self.infotext = QLabel("""Developers : Dummerle, CommandMC\nLegendary Dev: Derrod\nLicence: GPL v3""")

        self.layout.addWidget(self.info_label)
        self.layout.addWidget(self.infotext)
        self.layout.addStretch(1)
        self.setLayout(self.layout)

    def logout(self):
        logout()
        exit(0)


class GameListInstalled(QScrollArea):
    def __init__(self, parent):
        super(GameListInstalled, self).__init__(parent=parent)
        self.widget = QWidget()
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.layout = QVBoxLayout()
        self.widgets = {}
        for i in get_installed():
            widget = GameWidget(i)
            widget.signal.connect(self.remove_game)
            self.widgets[i.app_name] = widget
            self.layout.addWidget(widget)
        self.widget.setLayout(self.layout)
        self.setWidget(self.widget)

    def remove_game(self, app_name: str):
        logger.info(f"Uninstall {app_name}")
        self.layout.removeWidget(self.widgets[app_name])
        self.widgets[app_name].deleteLater()
        self.widgets.pop(app_name)


class GameListUninstalled(QScrollArea):
    def __init__(self, parent):
        super(GameListUninstalled, self).__init__(parent=parent)
        self.widget = QWidget()
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.layout = QVBoxLayout()

        self.filter = QLineEdit()
        self.filter.setPlaceholderText("Search game TODO")
        self.layout.addWidget(self.filter)

        self.widgets = []
        for game in get_not_installed():
            game_widget = UninstalledGameWidget(game)
            self.layout.addWidget(game_widget)
            self.widgets.append(game_widget)
        self.widget.setLayout(self.layout)
        self.setWidget(self.widget)


class UpdateList(QWidget):
    def __init__(self, parent):
        super(UpdateList, self).__init__(parent=parent)
        self.layout = QVBoxLayout()
        updates = get_updates()
        if not updates:
            for game in get_updates():
                self.layout.addWidget(QLabel("Update available for " + game.title))

        else:
            self.layout.addWidget(QLabel("No updates available"))
        self.layout.addStretch(1)
        self.setLayout(self.layout)
