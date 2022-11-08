import time
from logging import getLogger
from typing import Tuple, Dict

from PyQt5.QtCore import Qt, QSettings, pyqtSlot
from PyQt5.QtWidgets import QStackedWidget, QVBoxLayout, QWidget, QScrollArea, QFrame
from legendary.models.game import Game

from rare.models.game import RareGame
from rare.shared import LegendaryCoreSingleton, GlobalSignalsSingleton, ArgumentsSingleton
from rare.shared.rare_core import RareCoreSingleton
from rare.widgets.library_layout import LibraryLayout
from rare.widgets.sliding_stack import SlidingStackedWidget
from .cloud_save_utils import CloudSaveUtils
from .game_info import GameInfoTabs
from .game_info.uninstalled_info import UninstalledInfoTabs
from .game_utils import GameUtils
from .game_widgets import LibraryWidgetController
from .game_widgets.icon_game_widget import IconGameWidget
from .game_widgets.list_game_widget import ListGameWidget
from .head_bar import GameListHeadBar
from .import_sync import ImportSyncTabs

logger = getLogger("GamesTab")


class GamesTab(QStackedWidget):
    widgets: Dict[str, Tuple[IconGameWidget, ListGameWidget]] = dict()
    active_filter = 0

    def __init__(self, parent=None):
        super(GamesTab, self).__init__(parent=parent)
        self.core = LegendaryCoreSingleton()
        self.signals = GlobalSignalsSingleton()
        self.args = ArgumentsSingleton()
        self.rare_core = RareCoreSingleton()
        self.settings = QSettings()

        self.game_utils = GameUtils(parent=self)

        self.games = QWidget(parent=self)
        self.games.setLayout(QVBoxLayout())
        self.addWidget(self.games)

        self.head_bar = GameListHeadBar(parent=self.games)
        self.head_bar.import_clicked.connect(self.show_import)
        self.head_bar.egl_sync_clicked.connect(self.show_egl_sync)
        self.games.layout().addWidget(self.head_bar)

        self.game_info_tabs = GameInfoTabs(self.rare_core.dlcs, self.game_utils, self)
        self.game_info_tabs.back_clicked.connect(lambda: self.setCurrentWidget(self.games))
        self.addWidget(self.game_info_tabs)

        self.import_sync_tabs = ImportSyncTabs(self)
        self.import_sync_tabs.back_clicked.connect(lambda: self.setCurrentWidget(self.games))
        self.addWidget(self.import_sync_tabs)

        self.uninstalled_info_tabs = UninstalledInfoTabs(self)
        self.uninstalled_info_tabs.back_clicked.connect(lambda: self.setCurrentIndex(0))
        self.addWidget(self.uninstalled_info_tabs)

        self.view_stack = SlidingStackedWidget(self.games)
        self.view_stack.setFrameStyle(QFrame.NoFrame)
        self.icon_view_scroll = QScrollArea(self.view_stack)
        self.icon_view_scroll.setWidgetResizable(True)
        self.icon_view_scroll.setFrameShape(QFrame.StyledPanel)
        self.icon_view_scroll.horizontalScrollBar().setDisabled(True)
        self.list_view_scroll = QScrollArea(self.view_stack)
        self.list_view_scroll.setWidgetResizable(True)
        self.list_view_scroll.setFrameShape(QFrame.StyledPanel)
        self.list_view_scroll.horizontalScrollBar().setDisabled(True)
        self.icon_view = QWidget(self.icon_view_scroll)
        self.icon_view.setLayout(LibraryLayout(self.icon_view))
        self.icon_view.layout().setContentsMargins(0, 13, 0, 0)
        self.icon_view.layout().setAlignment(Qt.AlignTop)
        self.list_view = QWidget(self.list_view_scroll)
        self.list_view.setLayout(QVBoxLayout(self.list_view))
        self.list_view.layout().setContentsMargins(3, 3, 9, 3)
        self.list_view.layout().setAlignment(Qt.AlignTop)
        self.library_controller = LibraryWidgetController(
            self.icon_view, self.list_view, self.game_utils, self
        )
        self.icon_view_scroll.setWidget(self.icon_view)
        self.list_view_scroll.setWidget(self.list_view)
        self.view_stack.addWidget(self.icon_view_scroll)
        self.view_stack.addWidget(self.list_view_scroll)
        self.games.layout().addWidget(self.view_stack)

        if not self.settings.value("icon_view", True, bool):
            self.view_stack.setCurrentWidget(self.list_view_scroll)
            self.head_bar.view.list()
        else:
            self.view_stack.setCurrentWidget(self.icon_view_scroll)

        self.head_bar.search_bar.textChanged.connect(lambda x: self.filter_games("", x))
        self.head_bar.search_bar.textChanged.connect(
            lambda x: self.icon_view_scroll.verticalScrollBar().setSliderPosition(
                self.icon_view_scroll.verticalScrollBar().minimum()
            )
        )
        self.head_bar.search_bar.textChanged.connect(
            lambda x: self.list_view_scroll.verticalScrollBar().setSliderPosition(
                self.list_view_scroll.verticalScrollBar().minimum()
            )
        )
        self.head_bar.filterChanged.connect(self.filter_games)
        self.head_bar.refresh_list.clicked.connect(self.library_controller.update_list)
        self.head_bar.view.toggled.connect(self.toggle_view)

        f = self.settings.value("filter", 0, int)
        if f >= len(self.head_bar.available_filters):
            f = 0
        self.active_filter = self.head_bar.available_filters[f]

        # signals
        self.signals.game.installed.connect(self.update_count_games_label)
        self.signals.game.uninstalled.connect(self.update_count_games_label)
        self.signals.game.uninstalled.connect(lambda x: self.setCurrentIndex(0))

        # self.signals.update_gamelist.connect(self.library_controller.update_list)
        # self.game_utils.update_list.connect(self.library_controller.update_list)

        start_t = time.time()
        self.setup_game_list()
        print(f"Game list setup time: {time.time() - start_t}")

    def show_import(self):
        self.setCurrentWidget(self.import_sync_tabs)
        self.import_sync_tabs.show_import()

    def show_egl_sync(self, idx):
        self.setCurrentWidget(self.import_sync_tabs)
        self.import_sync_tabs.show_egl_sync()

    @pyqtSlot(Game, bool)
    def show_game_info(self, game, installed):
        if installed:
            self.game_info_tabs.update_game(game.app_name)
            self.setCurrentWidget(self.game_info_tabs)
        else:
            self.uninstalled_info_tabs.update_game(game)
            self.setCurrentWidget(self.uninstalled_info_tabs)

    def show_uninstalled_info(self, game):
        self.uninstalled_info_tabs.update_game(game)
        self.setCurrentWidget(self.uninstalled_info_tabs)

    @pyqtSlot()
    def update_count_games_label(self):
        self.head_bar.set_games_count(
            len([game for game in self.rare_core.games if game.is_installed]),
            len([game for game in self.rare_core.games])
        )

    def setup_game_list(self):
        self.update_count_games_label()
        for rgame in self.rare_core.games:
            icon_widget, list_widget = self.add_library_widget(rgame)
            if not icon_widget or not list_widget:
                logger.warning(f"Ignoring {rgame.app_name} in game list")
                continue
            self.icon_view.layout().addWidget(icon_widget)
            self.list_view.layout().addWidget(list_widget)
        self.filter_games(self.active_filter)

    def add_library_widget(self, game: RareGame):
        try:
            icon_widget, list_widget = self.library_controller.add_game(game, self.game_utils)
        except Exception as e:
            # FIXME
            raise e
            logger.error(f"{app_name} is broken. Don't add it to game list: {e}")
            return None, None

        self.widgets[game.app_name] = (icon_widget, list_widget)

        icon_widget.show_info.connect(self.show_game_info)
        list_widget.show_info.connect(self.show_game_info)

        return icon_widget, list_widget

    @pyqtSlot(str)
    @pyqtSlot(str, str)
    def filter_games(self, filter_name="all", search_text: str = ""):
        if not search_text and (t := self.head_bar.search_bar.text()):
            search_text = t

        if filter_name:
            self.active_filter = filter_name
        if not filter_name and (t := self.active_filter):
            filter_name = t

        self.library_controller.filter_list(filter_name, search_text.lower())

    def toggle_view(self):
        self.settings.setValue("icon_view", not self.head_bar.view.isChecked())

        if not self.head_bar.view.isChecked():
            self.view_stack.slideInWidget(self.icon_view_scroll)
        else:
            self.view_stack.slideInWidget(self.list_view_scroll)
