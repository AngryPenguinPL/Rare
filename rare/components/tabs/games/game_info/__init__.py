from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent

from rare.components.tabs.games.game_utils import GameUtils
from rare.shared import LegendaryCoreSingleton, GlobalSignalsSingleton
from rare.utils.extra_widgets import SideTabWidget
from .cloud_saves import CloudSavesTab
from .game_dlc import GameDlc
from .game_info import GameInfo
from .game_settings import GameSettings


class GameInfoTabs(SideTabWidget):
    def __init__(self, dlcs: dict, game_utils: GameUtils, parent=None):
        super(GameInfoTabs, self).__init__(show_back=True, parent=parent)
        self.core = LegendaryCoreSingleton()
        self.signals = GlobalSignalsSingleton()

        self.info = GameInfo(self, game_utils)
        self.addTab(self.info, self.tr("Information"))

        self.settings = GameSettings(self)
        self.addTab(self.settings, self.tr("Settings"))

        self.cloud_saves_tab = CloudSavesTab(self)
        self.addTab(self.cloud_saves_tab, self.tr("Cloud Saves"))

        self.dlc_list = dlcs
        self.dlc = GameDlc(self.dlc_list, game_utils, self)
        self.addTab(self.dlc, self.tr("Downloadable Content"))

        self.tabBar().setCurrentIndex(1)

    def update_game(self, app_name: str):
        self.setCurrentIndex(1)
        self.info.update_game(app_name)
        self.settings.load_settings(app_name)
        self.cloud_saves_tab.update_game(app_name)

        # DLC Tab: Disable if no dlcs available
        if (
                len(self.dlc_list.get(self.core.get_game(app_name).catalog_item_id, []))
                == 0
        ):
            self.setTabEnabled(4, False)
        else:
            self.setTabEnabled(4, True)
            self.dlc.update_dlcs(app_name)

    def keyPressEvent(self, e: QKeyEvent):
        if e.key() == Qt.Key_Escape:
            self.back_clicked.emit()
