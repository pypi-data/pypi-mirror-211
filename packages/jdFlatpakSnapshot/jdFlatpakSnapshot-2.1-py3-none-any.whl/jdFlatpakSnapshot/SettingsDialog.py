from .ui_compiled.SettingsDialog import Ui_SettingsDialog
from .Functions import select_combo_box_data
from .Languages import get_language_names
from PyQt6.QtCore import QCoreApplication
from PyQt6.QtWidgets import QDialog
from typing import TYPE_CHECKING
from .Settings import Settings
import datetime
import os


if TYPE_CHECKING:
    from .Environment import Environment
    from .MainWindow import MainWindow


class SettingsDialog(QDialog, Ui_SettingsDialog):
    def __init__(self, env: "Environment", main_window: "MainWindow") -> None:
        super().__init__()

        self.setupUi(self)

        self._env = env
        self._main_window = main_window

        language_names = get_language_names()
        self.language_box.addItem(QCoreApplication.translate("SettingsDialog", "System language"), "default")
        self.language_box.addItem(language_names["en"], "en")
        for i in os.listdir(os.path.join(env.program_dir, "translations")):
            if not i.endswith(".qm"):
                continue

            lang = i.removeprefix("jdFlatpakSnapshot_").removesuffix(".qm")
            self.language_box.addItem(language_names.get(lang, lang), lang)

        if self.language_box.count() == 2:
            print("No compiled translations found. Please run tools/BuildTranslations to build the Translations.py.")

        self.datetime_format_edit.textChanged.connect(self._update_datetime_preview)

        self.reset_button.clicked.connect(lambda: self._update_widgets(Settings()))
        self.ok_button.clicked.connect(self._ok_button_clicked)
        self.cancel_button.clicked.connect(self.close)

    def _update_widgets(self, settings: Settings) -> None:
        select_combo_box_data(self.language_box, settings.get("language"))
        self.datetime_format_edit.setText(settings.get("datetimeFormat"))
        self.show_system_apps_check_box.setChecked(settings.get("showSystemApps"))
        self.show_apps_with_no_data_check_box.setChecked(settings.get("showAppsWithNoData"))
        self.allow_creating_while_running_check_box.setChecked(settings.get("allowCreatingWhileRunning"))
        self.allow_restoring_while_running_check_box.setChecked(settings.get("allowRestoringWhileRunning"))
        self.flatpak_command_edit.setText(settings.get("flatpakCommand"))

    def _update_datetime_preview(self):
        try:
            format = datetime.datetime.now().strftime(self.datetime_format_edit.text())
            self.datetime_format_preview_label.setText(QCoreApplication.translate("SettingsDialog", "(Preview: {{preview}})").replace("{{preview}}", format))
        except ValueError:
            self.datetime_format_preview_label.setText(QCoreApplication.translate("SettingsDialog", "(Invalid)"))

    def _ok_button_clicked(self) -> None:
        self._env.settings.set("language", self.language_box.currentData())
        self._env.settings.set("datetimeFormat", self.datetime_format_edit.text())
        self._env.settings.set("showSystemApps", self.show_system_apps_check_box.isChecked())
        self._env.settings.set("showAppsWithNoData", self.show_apps_with_no_data_check_box.isChecked())
        self._env.settings.set("allowCreatingWhileRunning", self.allow_creating_while_running_check_box.isChecked())
        self._env.settings.set("allowRestoringWhileRunning", self.allow_restoring_while_running_check_box.isChecked())
        self._env.settings.set("flatpakCommand", self.flatpak_command_edit.text())

        self._env.settings.save(os.path.join(self._env.data_dir, "settings.json"))
        self._main_window.update_app_list_visible()
        self.close()

    def open_dialog(self) -> None:
        self._update_widgets(self._env.settings)
        self.exec()