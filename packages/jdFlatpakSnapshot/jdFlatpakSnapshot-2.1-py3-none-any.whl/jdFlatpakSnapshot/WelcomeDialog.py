from .ui_compiled.WelcomeDialog import Ui_WelcomeDialog
from PyQt6.QtWidgets import QDialog
from typing import TYPE_CHECKING
import os


if TYPE_CHECKING:
    from .Environment import Environment


class WelcomeDialog(QDialog, Ui_WelcomeDialog):
    def __init__(self, env: "Environment") -> None:
        super().__init__()
        self._env = env

        self.setupUi(self)

    def open_dialog(self) -> None:
        self.show_startup_check_box.setChecked(self._env.settings.get("showWelcomeDialog"))
        self.exec()
        self._env.settings.set("showWelcomeDialog", self.show_startup_check_box.isChecked())
        self._env.settings.save(os.path.join(self._env.data_dir, "settings.json"))