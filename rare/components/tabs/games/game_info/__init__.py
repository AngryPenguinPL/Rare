from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from legendary.models.game import Game

import rare.shared as shared
from rare.utils.extra_widgets import SideTabWidget
from .game_dlc import GameDlc
from .game_info import GameInfo
from .game_settings import GameSettings


class GameInfoTabs(SideTabWidget):
    def __init__(self, dlcs: list, parent=None):
        super(GameInfoTabs, self).__init__(show_back=True, parent=parent)
        self.core = shared.legendary_core
        self.signals = shared.signals

        self.info = GameInfo(self.core, self.signals, self)
        self.addTab(self.info, self.tr("Information"))

        self.settings = GameSettings(self.core, self)
        self.addTab(self.settings, self.tr("Settings"))

        self.dlc_list = dlcs
        self.dlc = GameDlc(self.dlc_list, self)
        self.addTab(self.dlc, self.tr("Downloadable Content"))

        self.tabBar().setCurrentIndex(1)

    def update_game(self, game: Game, dlcs: list):
        self.setCurrentIndex(1)
        self.info.update_game(game)
        self.settings.update_game(game)

        # DLC Tab: Disable if no dlcs available
        if len(self.dlc_list[game.asset_info.catalog_item_id]) == 0:
            self.setTabEnabled(3, False)
        else:
            self.setTabEnabled(3, True)
            self.dlc.update_dlcs(game.app_name)

    def keyPressEvent(self, e: QKeyEvent):
        if e.key() == Qt.Key_Escape:
            self.parent().layout().setCurrentIndex(0)
