import json
import os
import platform
import sys
import time
from enum import IntEnum
from itertools import chain
from logging import getLogger
from typing import Dict, Iterator, Callable, Tuple, Optional
from typing import List

from PyQt5.QtCore import QObject, pyqtSignal, QRunnable, QSettings, pyqtSlot, QThreadPool, QStandardPaths
from legendary.models.game import Game, SaveGameFile, InstalledGame
from requests.exceptions import ConnectionError, HTTPError

from rare.components.dialogs.uninstall_dialog import UninstallDialog
from rare.lgndr.api_arguments import LgndrUninstallGameArgs
from rare.lgndr.api_monkeys import LgndrIndirectStatus
from rare.lgndr.cli import LegendaryCLI
from rare.models.game import RareGame
from rare.shared import LegendaryCoreSingleton, ArgumentsSingleton
from rare.shared.image_manager import ImageManagerSingleton
from rare.utils.paths import data_dir
from rare.utils import config_helper

logger = getLogger("RareCore")


class RareCore(QObject):
    class Worker(QRunnable):
        class Result(IntEnum):
            GAMES = 1
            NON_ASSET = 2
            WIN32 = 3
            MACOS = 4
            SAVES = 5

        class Signals(QObject):
            result = pyqtSignal(object, int)

        def __init__(self):
            sys.excepthook = sys.__excepthook__
            super(RareCore.Worker, self).__init__()
            self.setAutoDelete(True)

            self.signals = RareCore.Worker.Signals()
            self.core = LegendaryCoreSingleton()
            self.args = ArgumentsSingleton()

        def run(self):
            pass

    class GamesWorker(Worker):
        def run(self):
            start_time = time.time()
            result = self.core.get_game_and_dlc_list(
                update_assets=not self.args.offline,
                platform="Windows",
                skip_ue=False,
            )
            self.signals.result.emit(result, RareCore.Worker.Result.GAMES)
            logger.debug(f"Games: {len(result[0])}, DLCs {len(result[1])}")
            logger.debug(f"Request Games: {time.time() - start_time} seconds")

    class NonAssetWorker(Worker):
        def run(self):
            start_time = time.time()
            try:
                result = self.core.get_non_asset_library_items(force_refresh=False, skip_ue=False)
            except (HTTPError, ConnectionError) as e:
                logger.warning(f"Exception while fetching non asset games from EGS: {e}")
                result = ([], {})
            self.signals.result.emit(result, RareCore.Worker.Result.NON_ASSET)
            logger.debug(f"Non asset: {len(result[0])}, DLCs {len(result[1])}")
            logger.debug(f"Request Non Asset: {time.time() - start_time} seconds")

    class Win32Worker(Worker):
        def run(self):
            start_time = time.time()
            result = self.core.get_game_and_dlc_list(
                update_assets=False, platform="Win32", skip_ue=False
            )
            self.signals.result.emit(([], {}), RareCore.Worker.Result.WIN32)
            logger.debug(f"Win32: {len(result[0])}, DLCs {len(result[1])}")
            logger.debug(f"Request Win32: {time.time() - start_time} seconds")

    class MacOSWorker(Worker):
        def run(self):
            start_time = time.time()
            result = self.core.get_game_and_dlc_list(
                update_assets=False, platform="Mac", skip_ue=False
            )
            self.signals.result.emit(([], {}), RareCore.Worker.Result.MACOS)
            logger.debug(f"MacOS: {len(result[0])}, DLCs {len(result[1])}")
            logger.debug(f"Request MacOS: {time.time() - start_time} seconds")

    class SavesWorker(Worker):
        def run(self):
            start_time = time.time()
            try:
                result = self.core.get_save_games()
            except (HTTPError, ConnectionError) as e:
                logger.warning(f"Exception while fetching saves fromt EGS: {e}")
                result = list()
            self.signals.result.emit((result, {}), RareCore.Worker.Result.SAVES)
            logger.debug(f"Saves: {len(result)}")
            logger.debug(f"Request saves: {time.time() - start_time} seconds")

    __games: Dict[str, RareGame] = dict()
    __games_fetched: bool = False
    __non_asset_fetched: bool = False
    __win32_fetched: bool = False
    __macos_fetched: bool = False
    __saves_fetched: bool = False

    completed = pyqtSignal()
    progress = pyqtSignal(int, str)

    def __init__(self):
        super(RareCore, self).__init__()
        self.core = LegendaryCoreSingleton()
        self.args = ArgumentsSingleton()
        self.image_manager = ImageManagerSingleton()
        self.settings = QSettings()
        self.threadpool = QThreadPool.globalInstance()

    def load_metadata(self):
        try:
            with open(os.path.join(data_dir, "game_meta.json")) as metadata_json:
                metadata = json.load(metadata_json)
        except FileNotFoundError:
            logger.info("Game metadata json file does not exist.")
        except json.JSONDecodeError:
            logger.warning("Game metadata json file is corrupt.")
        else:
            for app_name, data in metadata.items():
                self.__games[app_name].metadata = RareGame.Metadata.from_json(data)

    def save_metadata(self):
        with open(os.path.join(data_dir, "game_meta.json"), "w") as metadata_json:
            json.dump(
                {
                    app_name: game.metadata.__dict__()
                    for app_name, game in self.__games.items()
                    if game.metadata
                },
                metadata_json,
                indent=2,
            )

    def uninstall_game(self, igame: InstalledGame, keep_files=False, keep_config=False):
        # remove shortcuts link
        desktop = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)
        applications = QStandardPaths.writableLocation(QStandardPaths.ApplicationsLocation)
        if platform.system() == "Linux":
            desktop_shortcut = os.path.join(desktop, f"{igame.title}.desktop")
            if os.path.exists(desktop_shortcut):
                os.remove(desktop_shortcut)

            applications_shortcut = os.path.join(applications, f"{igame.title}.desktop")
            if os.path.exists(applications_shortcut):
                os.remove(applications_shortcut)

        elif platform.system() == "Windows":
            game_title = igame.title.split(":")[0]
            desktop_shortcut = os.path.join(desktop, f"{game_title}.lnk")
            if os.path.exists(desktop_shortcut):
                os.remove(desktop_shortcut)

            start_menu_shortcut = os.path.join(applications, "..", f"{game_title}.lnk")
            if os.path.exists(start_menu_shortcut):
                os.remove(start_menu_shortcut)

        status = LgndrIndirectStatus()
        LegendaryCLI(self.core).uninstall_game(
            LgndrUninstallGameArgs(
                app_name=igame.app_name,
                keep_files=keep_files,
                indirect_status=status,
                yes=True,
            )
        )
        if not keep_config:
            logger.info("Removing sections in config file")
            config_helper.remove_section(igame.app_name)
            config_helper.remove_section(f"{igame.app_name}.env")

            config_helper.save_config()

        return status.success, status.message

    def uninstall_game(self, app_name) -> bool:
        # returns if uninstalled
        game = self.core.get_game(app_name)
        igame = self.core.get_installed_game(app_name)
        if not os.path.exists(igame.install_path):
            if QMessageBox.Yes == QMessageBox.question(
                    None,
                    self.tr("Uninstall - {}").format(igame.title),
                    self.tr(
                        "Game files of {} do not exist. Remove it from installed games?"
                    ).format(igame.title),
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.Yes,
            ):
                self.core.lgd.remove_installed_game(app_name)
                return True
            else:
                return False

        proceed, keep_files, keep_config = UninstallDialog(game).get_options()
        if not proceed:
            return False
        success, message = legendary_utils.uninstall_game(self.core, game.app_name, keep_files, keep_config)
        if not success:
            QMessageBox.warning(None, self.tr("Uninstall - {}").format(igame.title), message, QMessageBox.Close)
        self.signals.game_uninstalled.emit(app_name)
        return True

    def verify_install_status(self):
        for rgame in self.__filter_games(lambda rg: rg.igame is not None and not rg.is_dlc):
            if not os.path.exists(rgame.igame.install_path):
                # lk; since install_path is lost anyway, set keep_files to True
                # lk: to avoid spamming the log with "file not found" errors
                for dlc in rgame.owned_dlcs:
                    if dlc.is_installed:
                        logger.info(f'Uninstalling DLC "{dlc.app_name}" ({dlc.app_title})...')
                        self.uninstall_game(dlc.igame, keep_files=True)
                        dlc.igame = None
                logger.info(
                    f'Removing "{rgame.app_title}" because "{rgame.igame.install_path}" does not exist...'
                )
                self.uninstall_game(rgame.igame, keep_files=True)
                logger.info(f"Uninstalled {rgame.app_title}, because no game files exist")
                rgame.igame = None
                continue
            # lk: games that don't have an override and can't find their executable due to case sensitivity
            # lk: will still erroneously require verification. This might need to be removed completely
            # lk: or be decoupled from the verification requirement
            if override_exe := self.core.lgd.config.get(rgame.app_name, "override_exe", fallback=""):
                igame_executable = override_exe
            else:
                igame_executable = rgame.igame.executable
            if not os.path.exists(
                    os.path.join(rgame.igame.install_path, igame_executable.replace("\\", "/").lstrip("/"))):
                rgame.igame.needs_verification = True
                self.core.lgd.set_installed_game(rgame.app_name, rgame.igame)
                logger.info(f"{rgame.app_title} needs verification")

    def get_game(self, app_name: str) -> RareGame:
        return self.__games[app_name]

    def add_game(self, game: Game) -> None:
        if game.app_name not in self.__games:
            self.__games[game.app_name] = RareGame(game)
        else:
            logger.warning(f"{game.app_name} already present in {type(self).__name__}")
            logger.info(f"Updating Game for {game.app_name}")
            self.__games[game.app_name].game = game

    def __add_games_and_dlcs(self, games_list: List[Game], dlcs_dict: Dict[str, List]) -> None:
        for game in games_list:
            self.add_game(game)
        for catalog_item_id, dlcs in dlcs_dict.items():
            rare_game_dlcs = [RareGame(dlc) for dlc in dlcs]
            for dlc in rare_game_dlcs:
                self.__games[dlc.app_name] = dlc
            # FIXME: find a better way to do this maybe?
            main_game = next(self.__filter_games(lambda g: g.game.catalog_item_id == catalog_item_id))
            main_game.owned_dlcs.extend(rare_game_dlcs)

    @pyqtSlot(object, int)
    def handle_result(self, result: Tuple, res_type: int):
        status = str()
        if res_type == RareCore.Worker.Result.GAMES:
            logger.debug(f"Got Api Results for GAMES")
            games, dlc_dict = result
            self.__add_games_and_dlcs(games, dlc_dict)
            self.__games_fetched = True
            status = "Loaded games for Windows"
        if res_type == RareCore.Worker.Result.NON_ASSET:
            logger.debug(f"Got Api Results for NON_ASSET")
            games, dlc_dict = result
            self.__add_games_and_dlcs(games, dlc_dict)
            self.__non_asset_fetched = True
            status = "Loaded games without assets"
        if res_type == RareCore.Worker.Result.WIN32:
            logger.debug(f"Got Api Results for WIN32")
            self.__win32_fetched = True
            status = "Loaded games for Windows (32bit)"
        if res_type == RareCore.Worker.Result.MACOS:
            logger.debug(f"Got Api Results for MACOS")
            self.__macos_fetched = True
            status = "Loaded games for MacOS"
        if res_type == RareCore.Worker.Result.SAVES:
            logger.debug(f"Got Api Results for SAVES")
            saves, _ = result
            for save in saves:
                self.__games[save.app_name].saves.append(save)
            self.__saves_fetched = True
            status = "Loaded save games"

        fetched = [
            self.__games_fetched,
            self.__non_asset_fetched,
            self.__win32_fetched,
            self.__macos_fetched,
            self.__saves_fetched,
        ]

        self.progress.emit(sum(fetched) * 10, status)

        if all(fetched):
            self.progress.emit(70, "Verifying game file status")
            self.verify_install_status()
            self.progress.emit(90, "Loading game metadata for Rare")
            self.load_metadata()
            self.progress.emit(100, "Loading completed, launching Rare")
            logger.debug(f"Fetch time {time.time() - self.start_time} seconds")
            self.completed.emit()

    def fetch(self):
        self.__games_fetched: bool = False
        self.__non_asset_fetched: bool = False
        self.__win32_fetched: bool = False
        self.__macos_fetched: bool = False
        self.__saves_fetched: bool = False

        self.start_time = time.time()
        games_worker = RareCore.GamesWorker()
        games_worker.signals.result.connect(self.handle_result)
        games_worker.signals.result.connect(self.fetch_saves)
        games_worker.signals.result.connect(self.fetch_extra)
        self.threadpool.start(games_worker)

    def fetch_saves(self):
        if not self.args.offline:
            saves_worker = RareCore.SavesWorker()
            saves_worker.signals.result.connect(self.handle_result)
            self.threadpool.start(saves_worker)
        else:
            self.__saves_fetched = True

    def fetch_extra(self):
        non_asset_worker = RareCore.NonAssetWorker()
        non_asset_worker.signals.result.connect(self.handle_result)
        self.threadpool.start(non_asset_worker)

        if self.settings.value("win32_meta", False, bool):
            win32_worker = RareCore.Win32Worker()
            win32_worker.signals.result.connect(self.handle_result)
            self.threadpool.start(win32_worker)
        else:
            self.__win32_fetched = True

        if self.settings.value("mac_meta", platform.system() == "Darwin", bool):
            macos_worker = RareCore.MacOSWorker()
            macos_worker.signals.result.connect(self.handle_result)
            self.threadpool.start(macos_worker)
        else:
            self.__macos_fetched = True

    def load_pixmaps(self) -> None:
        """
        Load pixmaps for all games

        This exists here solely to fight signal and possibly threading issues.
        The initial image loading at startup should not be done in the RareGame class
        for two reasons. It will delay startup due to widget updates and the image
        might become availabe before the UI is brought up. In case of the second, we
        will get both a long queue of signals to be serviced and some of them might
        be not connected yet and the widget won't be updated. So do the loading here
        by calling this after the MainWindow has finished initializing.

        @return: None
        """
        self.threadpool.start(self.__load_pixmaps)

    def __load_pixmaps(self) -> None:
        # time.sleep(0.1)
        for rgame in self.__games.values():
            rgame.set_pixmap()
            # time.sleep(0.0001)

    def __filter_games(self, condition: Callable[[RareGame], bool]) -> Iterator[RareGame]:
        return filter(condition, self.__games.values())

    @property
    def games_and_dlcs(self) -> Iterator[RareGame]:
        for app_name in self.__games:
            yield self.__games[app_name]

    @property
    def games(self) -> Iterator[RareGame]:
        return self.__filter_games(lambda game: not game.is_dlc)

    @property
    def game_list(self) -> Iterator[Game]:
        for game in self.games:
            yield game.game

    @property
    def dlcs(self) -> Dict[str, Game]:
        """!
        RareGames that ARE DLCs themselves
        """
        return {game.game.catalog_item_id: game.owned_dlcs for game in self.has_dlcs}
        # return self.__filter_games(lambda game: game.is_dlc)

    @property
    def has_dlcs(self) -> Iterator[RareGame]:
        """!
        RareGames that HAVE DLCs associated with them
        """
        return self.__filter_games(lambda game: bool(game.owned_dlcs))

    @property
    def bit32_games(self) -> Iterator[RareGame]:
        return self.__filter_games(lambda game: game.is_win32)

    @property
    def mac_games(self) -> Iterator[RareGame]:
        return self.__filter_games(lambda game: game.is_mac)

    @property
    def no_asset_games(self) -> Iterator[RareGame]:
        return self.__filter_games(lambda game: game.is_non_asset)

    @property
    def unreal_engine(self) -> Iterator[RareGame]:
        return self.__filter_games(lambda game: game.is_unreal)

    @property
    def updates(self) -> Iterator[RareGame]:
        return self.__filter_games(lambda game: game.has_update)

    @property
    def saves(self) -> Iterator[SaveGameFile]:
        """!
        SaveGameFiles across games
        """
        return chain.from_iterable([game.saves for game in self.has_saves])

    @property
    def has_saves(self) -> Iterator[RareGame]:
        """!
        RareGames that have SaveGameFiles associated with them
        """
        return self.__filter_games(lambda game: bool(game.saves))


_rare_core_singleton: Optional[RareCore] = None


def RareCoreSingleton(init: bool = False) -> RareCore:
    global _rare_core_singleton
    if _rare_core_singleton is None and not init:
        raise RuntimeError("Uninitialized use of RareCoreSingleton")
    if _rare_core_singleton is None:
        _rare_core_singleton = RareCore()
    return _rare_core_singleton
