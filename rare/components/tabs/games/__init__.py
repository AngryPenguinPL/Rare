import time
from logging import getLogger
from typing import Dict, List

from PyQt5.QtCore import QSettings, Qt, pyqtSlot
from PyQt5.QtWidgets import QStackedWidget, QVBoxLayout, QWidget, QScrollArea, QFrame
from legendary.models.game import Game

from rare.models.game import RareGame
from rare.shared import (
    LegendaryCoreSingleton,
    GlobalSignalsSingleton,
    ArgumentsSingleton,
    ApiResultsSingleton,
    ImageManagerSingleton,
)
from rare.shared import RareCore
from rare.widgets.library_layout import LibraryLayout
from rare.widgets.sliding_stack import SlidingStackedWidget
from .game_info import GameInfoTabs
from .game_widgets import LibraryWidgetController
from .game_widgets.icon_game_widget import IconGameWidget
from .game_widgets.list_game_widget import ListGameWidget
from .head_bar import GameListHeadBar
from .integrations import IntegrationsTabs

logger = getLogger("GamesTab")


class GamesTab(QStackedWidget):
    def __init__(self, parent=None):
        super(GamesTab, self).__init__(parent=parent)
        self.rcore = RareCore.instance()
        self.core = LegendaryCoreSingleton()
        self.signals = GlobalSignalsSingleton()
        self.args = ArgumentsSingleton()
        self.api_results = ApiResultsSingleton()
        self.image_manager = ImageManagerSingleton()
        self.settings = QSettings()

        self.active_filter: int = 0

        self.game_list: List[Game] = self.api_results.game_list
        self.dlcs: Dict[str, List[Game]] = self.api_results.dlcs
        self.no_assets: List[Game] = self.api_results.no_asset_games

        self.games_page = QWidget(parent=self)
        self.games_page.setLayout(QVBoxLayout())
        self.addWidget(self.games_page)

        self.head_bar = GameListHeadBar(parent=self.games_page)
        self.head_bar.goto_import.connect(self.show_import)
        self.head_bar.goto_egl_sync.connect(self.show_egl_sync)
        self.head_bar.goto_eos_ubisoft.connect(self.show_eos_ubisoft)
        self.games_page.layout().addWidget(self.head_bar)

        self.game_info_page = GameInfoTabs(self)
        self.game_info_page.back_clicked.connect(lambda: self.setCurrentWidget(self.games_page))
        self.addWidget(self.game_info_page)

        self.integrations_page = IntegrationsTabs(self)
        self.integrations_page.back_clicked.connect(lambda: self.setCurrentWidget(self.games_page))
        self.addWidget(self.integrations_page)

        self.no_asset_names = []
        if not self.args.offline:
            for game in self.no_assets:
                self.no_asset_names.append(game.app_name)
        else:
            self.no_assets = []

        self.view_stack = SlidingStackedWidget(self.games_page)
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
        self.library_controller = LibraryWidgetController(self.icon_view, self.list_view, self)
        self.icon_view_scroll.setWidget(self.icon_view)
        self.list_view_scroll.setWidget(self.list_view)
        self.view_stack.addWidget(self.icon_view_scroll)
        self.view_stack.addWidget(self.list_view_scroll)
        self.games_page.layout().addWidget(self.view_stack)

        if not self.settings.value("icon_view", True, bool):
            self.view_stack.setCurrentWidget(self.list_view_scroll)
            self.head_bar.view.list()
        else:
            self.view_stack.setCurrentWidget(self.icon_view_scroll)

        self.head_bar.search_bar.textChanged.connect(lambda x: self.filter_games("", x))
        self.head_bar.search_bar.textChanged.connect(self.scroll_to_top)
        self.head_bar.filterChanged.connect(self.filter_games)
        self.head_bar.filterChanged.connect(self.scroll_to_top)
        self.head_bar.refresh_list.clicked.connect(self.library_controller.update_list)
        self.head_bar.view.toggled.connect(self.toggle_view)

        f = self.settings.value("filter", 0, int)
        if f >= len(self.head_bar.available_filters):
            f = 0
        self.active_filter = self.head_bar.available_filters[f]

        # signals
        self.signals.game.installed.connect(self.update_count_games_label)
        self.signals.game.uninstalled.connect(self.update_count_games_label)

        start_t = time.time()
        self.setup_game_list()
        print(f"Game list setup time: {time.time() - start_t}")

    @pyqtSlot()
    def scroll_to_top(self):
        self.icon_view_scroll.verticalScrollBar().setSliderPosition(
            self.icon_view_scroll.verticalScrollBar().minimum()
        )
        self.list_view_scroll.verticalScrollBar().setSliderPosition(
            self.list_view_scroll.verticalScrollBar().minimum()
        )

    @pyqtSlot()
    def show_import(self):
        self.setCurrentWidget(self.integrations_page)
        self.integrations_page.show_import()

    @pyqtSlot()
    def show_egl_sync(self):
        self.setCurrentWidget(self.integrations_page)
        self.integrations_page.show_egl_sync()

    @pyqtSlot()
    def show_eos_ubisoft(self):
        self.setCurrentWidget(self.integrations_page)
        self.integrations_page.show_eos_ubisoft()

    @pyqtSlot(RareGame)
    def show_game_info(self, rgame):
        self.setCurrentWidget(self.game_info_page)
        self.game_info_page.update_game(rgame)

    @pyqtSlot()
    def update_count_games_label(self):
        self.head_bar.set_games_count(len(self.core.get_installed_list()), len(self.game_list))

    # FIXME: Remove this when RareCore is in place
    def __create_game_with_dlcs(self, game: Game) -> RareGame:
        rgame = RareGame(self.core, self.image_manager, game)
        if game_dlcs := self.dlcs[rgame.game.catalog_item_id]:
            for dlc in game_dlcs:
                rdlc = RareGame(self.core, self.image_manager, dlc)
                self.rcore.add_game(rdlc)
                # lk: plug dlc progress signals to the game's
                rdlc.signals.progress.start.connect(rgame.signals.progress.start)
                rdlc.signals.progress.update.connect(rgame.signals.progress.update)
                rdlc.signals.progress.finish.connect(rgame.signals.progress.finish)
                rdlc.set_pixmap()
                rgame.owned_dlcs.append(rdlc)
        return rgame

    def setup_game_list(self):
        self.update_count_games_label()
        for game in self.game_list + self.no_assets:
            rgame = self.__create_game_with_dlcs(game)
            self.rcore.add_game(rgame)
            icon_widget, list_widget = self.add_library_widget(rgame)
            if not icon_widget or not list_widget:
                logger.warning(f"Excluding {rgame.app_name} from the game list")
                continue
            self.icon_view.layout().addWidget(icon_widget)
            self.list_view.layout().addWidget(list_widget)
            rgame.set_pixmap()
        self.filter_games(self.active_filter)

    def add_library_widget(self, rgame: RareGame):
        try:
            icon_widget, list_widget = self.library_controller.add_game(rgame)
        except Exception as e:
            raise e
            logger.error(f"{rgame.app_name} is broken. Don't add it to game list: {e}")
            return None, None
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
