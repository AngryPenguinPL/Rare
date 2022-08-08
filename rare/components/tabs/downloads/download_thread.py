import os
import platform
import queue
import time
from dataclasses import dataclass
from enum import IntEnum
from logging import getLogger
from typing import List, Optional, Dict

from PyQt5.QtCore import QThread, pyqtSignal, QProcess
from legendary.core import LegendaryCore

from rare.lgndr.api_monkeys import DLManagerSignals
from rare.lgndr.cli import LegendaryCLI
from rare.lgndr.downloading import UIUpdate
from rare.models.install import InstallQueueItemModel
from rare.shared import GlobalSignalsSingleton

logger = getLogger("DownloadThread")


class DownloadThread(QThread):
    class ExitCode(IntEnum):
        ERROR = 1
        STOPPED = 2
        FINISHED = 3

    @dataclass
    class ExitStatus:
        app_name: str
        exit_code: int
        message: str = ""
        dlcs: Optional[List[Dict]] = None
        sync_saves: bool = False
        shortcuts: bool = False

    exit_status = pyqtSignal(ExitStatus)
    statistics = pyqtSignal(UIUpdate)

    def __init__(self, core: LegendaryCore, item: InstallQueueItemModel):
        super(DownloadThread, self).__init__()
        self.signals = GlobalSignalsSingleton()
        self.core: LegendaryCore = core
        self.item: InstallQueueItemModel = item
        self.dlm_signals: DLManagerSignals = DLManagerSignals()

    def run(self):
        _exit_status = DownloadThread.ExitStatus(self.item.download.game.app_name, DownloadThread.ExitCode.ERROR)
        start_t = time.time()
        try:
            self.item.download.dlmanager.start()
            time.sleep(1)
            while self.item.download.dlmanager.is_alive():
                try:
                    self.statistics.emit(self.item.download.dlmanager.status_queue.get(timeout=1.0))
                except queue.Empty:
                    pass
                if self.dlm_signals.update:
                    try:
                        self.item.download.dlmanager.signals_queue.put(self.dlm_signals, block=False, timeout=1.0)
                    except queue.Full:
                        pass
                time.sleep(self.item.download.dlmanager.update_interval/10)
            self.item.download.dlmanager.join()
        except Exception as e:
            end_t = time.time()
            logger.error(f"Installation failed after {end_t - start_t:.02f} seconds.")
            logger.warning(f"The following exception occurred while waiting for the downloader to finish: {e!r}.")
            _exit_status.exit_code = DownloadThread.ExitCode.ERROR
            _exit_status.message = f"{e!r}"
            self.exit_status.emit(_exit_status)
            return
        else:
            end_t = time.time()
            if self.dlm_signals.kill is True:
                logger.info(f"Download stopped after {end_t - start_t:.02f} seconds.")
                _exit_status.exit_code = DownloadThread.ExitCode.STOPPED
                self.exit_status.emit(_exit_status)
                return
            logger.info(f"Download finished in {end_t - start_t:.02f} seconds.")

            _exit_status.exit_code = DownloadThread.ExitCode.FINISHED

            if self.item.options.overlay:
                self.signals.overlay_installation_finished.emit()
                self.core.finish_overlay_install(self.item.download.igame)
                self.exit_status.emit(_exit_status)
                return

            if not self.item.options.no_install:
                postinstall = self.core.install_game(self.item.download.igame)
                if postinstall:
                    # LegendaryCLI(self.core)._handle_postinstall(
                    #     postinstall,
                    #     self.item.download.igame,
                    #     False,
                    #     self.item.options.install_preqs,
                    # )
                    self._handle_postinstall(postinstall, self.item.download.igame)

                dlcs = self.core.get_dlc_for_game(self.item.download.igame.app_name)
                if dlcs and not self.item.options.skip_dlcs:
                    for dlc in dlcs:
                        _exit_status.dlcs.append(
                            {"app_name": dlc.app_name, "app_title": dlc.app_title, "app_version": dlc.app_version}
                        )

                if self.item.download.game.supports_cloud_saves and not self.item.download.game.is_dlc:
                    _exit_status.sync_saves = True

            LegendaryCLI(self.core).clean_post_install(
                self.item.download.game,
                self.item.download.igame,
                self.item.download.repair,
                self.item.download.repair_file,
            )

            if not self.item.options.update and self.item.options.create_shortcut:
                _exit_status.shortcuts = True

        self.exit_status.emit(_exit_status)

    def _handle_postinstall(self, postinstall, igame):
        logger.info("This game lists the following prequisites to be installed:")
        logger.info(f'- {postinstall["name"]}: {" ".join((postinstall["path"], postinstall["args"]))}')
        if platform.system() == "Windows":
            if not self.item.options.install_preqs:
                logger.info('Marking prerequisites as installed...')
                self.core.prereq_installed(self.item.download.igame.app_name)
            else:
                logger.info('Launching prerequisite executable..')
                self.core.prereq_installed(igame.app_name)
                req_path, req_exec = os.path.split(postinstall["path"])
                work_dir = os.path.join(igame.install_path, req_path)
                fullpath = os.path.join(work_dir, req_exec)
                proc = QProcess()
                proc.setProcessChannelMode(QProcess.MergedChannels)
                proc.readyReadStandardOutput.connect(
                    lambda: logger.debug(str(proc.readAllStandardOutput().data(), "utf-8", "ignore"))
                )
                proc.setNativeArguments(postinstall.get("args", []))
                proc.setWorkingDirectory(work_dir)
                proc.start(fullpath)
                proc.waitForFinished()  # wait, because it is inside the thread
        else:
            logger.info("Automatic installation not available on Linux.")

    def kill(self):
        self.dlm_signals.kill = True
