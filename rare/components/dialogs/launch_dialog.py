import platform
from logging import getLogger

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QDialog, qApp
from requests.exceptions import ConnectionError

from rare.components.dialogs.login import LoginDialog
from rare.shared import LegendaryCoreSingleton, ArgumentsSingleton
from rare.shared.rare_core import RareCoreSingleton
from rare.ui.components.dialogs.launch_dialog import Ui_LaunchDialog

logger = getLogger("Login")


class LaunchDialog(QDialog):
    quit_app = pyqtSignal(int)
    start_app = pyqtSignal()
    accept_close = False

    def __init__(self, parent=None):
        super(LaunchDialog, self).__init__(parent=parent)
        self.ui = Ui_LaunchDialog()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setWindowFlags(
            Qt.Window
            | Qt.Dialog
            | Qt.CustomizeWindowHint
            | Qt.WindowSystemMenuHint
            | Qt.WindowTitleHint
            | Qt.WindowMinimizeButtonHint
            | Qt.MSWindowsFixedSizeDialogHint
        )
        self.setWindowModality(Qt.WindowModal)

        self.core = LegendaryCoreSingleton()
        self.args = ArgumentsSingleton()
        self.rare_core = RareCoreSingleton()
        self.rare_core.progress.connect(self.on_progress)
        self.rare_core.completed.connect(self.on_completed)

    def login(self):
        do_launch = True
        try:
            if self.args.offline:
                pass
            else:
                qApp.processEvents()
                if self.core.login():
                    logger.info("You are logged in")
                else:
                    raise ValueError("You are not logged in. Open Login Window")
        except ValueError as e:
            logger.info(str(e))
            # Do not set parent, because it won't show a task bar icon
            # Update: Inherit the same parent as LaunchDialog
            do_launch = LoginDialog(core=self.core, parent=self.parent()).login()
        except ConnectionError as e:
            logger.warning(e)
            self.args.offline = True
        finally:
            if do_launch:
                if not self.args.silent:
                    self.show()
                self.launch()
            else:
                self.quit_app.emit(0)

    def launch(self):
        self.rare_core.fetch()

    @pyqtSlot(int, str)
    def on_progress(self, prog: int, stat: str):
        self.ui.image_prog_bar.setValue(prog)
        self.ui.image_info.setText(stat)

    def on_completed(self):
        logger.info("App starting")
        self.ui.image_info.setText(self.tr("Starting..."))
        self.accept_close = True
        self.start_app.emit()

    def reject(self) -> None:
        if self.accept_close:
            super(LaunchDialog, self).reject()
        else:
            pass
