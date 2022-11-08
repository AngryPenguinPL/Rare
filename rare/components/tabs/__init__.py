from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMenu, QTabWidget, QWidget, QWidgetAction, QShortcut

from rare.shared import LegendaryCoreSingleton, GlobalSignalsSingleton, ArgumentsSingleton
from rare.components.tabs.account import AccountWidget
from rare.components.tabs.downloads import DownloadsTab
from rare.components.tabs.games import GamesTab
from rare.components.tabs.settings import SettingsTab
from rare.components.tabs.settings.debug import DebugSettings
from rare.components.tabs.shop import Shop
from rare.components.tabs.tab_utils import MainTabBar, TabButtonWidget
from rare.shared import LegendaryCoreSingleton, GlobalSignalsSingleton, ArgumentsSingleton
from rare.shared.rare_core import RareCoreSingleton
from rare.utils.misc import icon


class TabWidget(QTabWidget):
    def __init__(self, parent):
        super(TabWidget, self).__init__(parent=parent)
        self.core = LegendaryCoreSingleton()
        self.signals = GlobalSignalsSingleton()
        self.args = ArgumentsSingleton()
        self.rare_core = RareCoreSingleton()
        disabled_tab = 3 if not self.args.offline else 1
        self.setTabBar(MainTabBar(disabled_tab))
        # lk: Figure out why this adds a white line at the top
        # lk: despite setting qproperty-drawBase to 0 in the stylesheet
        # self.setDocumentMode(True)
        # Generate Tabs
        import time
        start_t = time.time()
        self.games_tab = GamesTab()
        self.addTab(self.games_tab, self.tr("Games"))
        print(f"Games Tab: {time.time() - start_t}")

        if not self.args.offline:
            # updates = self.games_tab.default_widget.game_list.updates
            start_t = time.time()
            updates = [u for u in self.rare_core.updates]
            self.downloads_tab = DownloadsTab(self)
            self.addTab(
                self.downloads_tab,
                self.tr("Downloads {}").format(f"({len(updates) if updates else 0})"),
            )
            print(f"Downloads Tab: {time.time() - start_t}")

            start_t = time.time()
            self.store = Shop(self.core)
            self.addTab(self.store, self.tr("Store (Beta)"))
            print(f"Store Tab: {time.time() - start_t}")

        start_t = time.time()
        self.settings = SettingsTab(self)
        if self.args.debug:
            self.settings.addTab(DebugSettings(), "Debug")
        print(f"Settings Tab: {time.time() - start_t}")

        # Space Tab
        self.addTab(QWidget(), "")
        self.setTabEnabled(disabled_tab, False)
        # Button
        self.account = QWidget()
        self.addTab(self.account, "")
        self.setTabEnabled(disabled_tab + 1, False)

        self.account_widget = AccountWidget()
        account_action = QWidgetAction(self)
        account_action.setDefaultWidget(self.account_widget)
        account_button = TabButtonWidget("mdi.account-circle", "Account", fallback_icon="fa.user")
        account_button.setMenu(QMenu())
        account_button.menu().addAction(account_action)
        self.tabBar().setTabButton(
            disabled_tab + 1, self.tabBar().RightSide, account_button
        )

        self.addTab(self.settings, icon("fa.gear"), "")

        self.settings.about.update_available_ready.connect(
            lambda: self.tabBar().setTabText(5, "(!)")
        )
        # Signals
        # set current index
        self.signals.set_main_tab_index.connect(self.setCurrentIndex)

        # update dl tab text
        self.signals.update_download_tab_text.connect(self.update_dl_tab_text)

        # Open game list on click on Games tab button
        self.tabBarClicked.connect(self.mouse_clicked)
        self.setIconSize(QSize(25, 25))

        # shortcuts
        QShortcut("Alt+1", self).activated.connect(lambda: self.setCurrentIndex(0))
        QShortcut("Alt+2", self).activated.connect(lambda: self.setCurrentIndex(1))
        QShortcut("Alt+3", self).activated.connect(lambda: self.setCurrentIndex(2))
        QShortcut("Alt+4", self).activated.connect(lambda: self.setCurrentIndex(5))

    def update_dl_tab_text(self):
        num_downloads = len(
            set(
                [i.options.app_name for i in self.downloads_tab.dl_queue]
                + [i for i in self.downloads_tab.update_widgets.keys()]
            )
        )

        if num_downloads != 0:
            self.setTabText(1, f"Downloads ({num_downloads})")
        else:
            self.setTabText(1, "Downloads")

    def mouse_clicked(self, tab_num):
        if tab_num == 0:
            self.games_tab.layout().setCurrentIndex(0)

        if not self.args.offline and tab_num == 2:
            self.store.load()

    def resizeEvent(self, event):
        self.tabBar().setMinimumWidth(self.width())
        super(TabWidget, self).resizeEvent(event)
