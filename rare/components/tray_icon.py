from logging import getLogger
from typing import List

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction

from rare.shared import GlobalSignalsSingleton
from rare.shared import LegendaryCoreSingleton
from rare.shared.rare_core import RareCoreSingleton

logger = getLogger("TrayIcon")


class TrayIcon(QSystemTrayIcon):
    def __init__(self, parent):
        super(TrayIcon, self).__init__(parent)
        self.core = LegendaryCoreSingleton()

        self.setIcon(QIcon(":/images/Rare.png"))
        self.setVisible(True)
        self.setToolTip("Rare")

        self.menu = QMenu()

        self.start_rare = QAction("Rare")
        self.menu.addAction(self.start_rare)

        self.menu.addSeparator()
        self.text_action = QAction("Quick launch")
        self.text_action.setEnabled(False)
        self.menu.addAction(self.text_action)

        self.rare_core = RareCoreSingleton()

        last_played = [game for game in self.rare_core.games if (game.metadata and game.is_installed)]
        last_played.sort(key=lambda g: g.metadata.last_played, reverse=True)
        last_played = last_played[0:5]

        # if len(installed := self.core.get_installed_list()) < 5:
        #     last_played = [GameMeta(i.app_name) for i in sorted(installed, key=lambda x: x.title)]
        # elif games := sorted(
        #         parent.mainwindow.tab_widget.games_tab.game_utils.game_meta.get_games(),
        #         key=lambda x: x.last_played, reverse=True):
        #     last_played: List[GameMeta] = games[0:5]
        # else:
        #     last_played = [GameMeta(i.app_name) for i in sorted(installed, key=lambda x: x.title)][0:5]

        self.game_actions: List[QAction] = []

        for game in last_played:
            a = QAction(game.game.app_title)
            a.setProperty("app_name", game.app_name)
            self.game_actions.append(a)
            a.triggered.connect(
                lambda: parent.mainwindow.tab_widget.games_tab.game_utils.prepare_launch(
                    self.sender().property("app_name"))
            )

        self.menu.addActions(self.game_actions)
        self.menu.addSeparator()

        self.exit_action = QAction(self.tr("Exit"))
        self.menu.addAction(self.exit_action)
        self.setContextMenu(self.menu)

        self.signals = GlobalSignalsSingleton()
        self.signals.game.uninstalled.connect(self.remove_button)

    def remove_button(self, app_name: str):
        if action := next((i for i in self.game_actions if i.property("app_name") == app_name), None):
            self.game_actions.remove(action)
            action.deleteLater()
