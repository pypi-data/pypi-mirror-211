from PyQt6.QtWidgets import QMainWindow, QListWidgetItem, QMessageBox, QInputDialog, QFileDialog, QApplication
from .ImportExport import import_file, export_single_snapshot
from.Functions import human_readable_size, format_datetime
from .Constants import FLATPAK_DIRS, COMPRESSION_METHODS
from .ui_compiled.MainWindow import Ui_MainWindow
from PyQt6.QtCore import Qt, QCoreApplication
from .SettingsDialog import SettingsDialog
from typing import Optional, TYPE_CHECKING
from .ProgressDialog import ProgressDialog
from .WelcomeDialog import WelcomeDialog
from .AboutDialog import AboutDialog
from PyQt6.QtGui import QIcon
import desktop_entry_lib
import webbrowser
import datetime
import shutil
import sys
import os


if TYPE_CHECKING:
    from .Environment import Environment
    from .Snapshot import Snapshot


def _get_name_from_desktop_entry(desktop_file: str, app_id: str, language: str) -> Optional[str]:
    try:
        entry = desktop_entry_lib.DesktopEntry.from_file(desktop_file)
    except Exception:
        return None

    if not entry.should_show():
        return None

    if entry.Name.default_text != "":
        if language == "default":
            return entry.Name.get_translated_text()
        else:
            return entry.Name.translations.get(language, entry.Name.default_text)
    else:
        return app_id


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, env: "Environment"):
        super().__init__()
        self._env = env

        self.setupUi(self)

        self._default_icon = QIcon(os.path.join(env.program_dir, "icons", "default-icon.svg"))
        self._settings_dialog = SettingsDialog(env, self)
        self._progress_dialog = ProgressDialog(env, self)
        self.welcome_dialog = WelcomeDialog(env)
        self._about_dialog = AboutDialog(env)

        self._fill_app_list()
        self._update_snapshot_buttons_enabled()

        self.list_apps.currentItemChanged.connect(self._list_apps_item_changed)
        self.snapshot_list.currentItemChanged.connect(self._update_snapshot_buttons_enabled)

        self.create_snapshot_button.clicked.connect(self._create_snapshot_button_clicked)
        self.restore_snapshot_button.clicked.connect(self._restore_snapshot_button_clicked)
        self.rename_snapshot_button.clicked.connect(self._rename_snapshot_button_clicked)
        self.delete_snapshot_button.clicked.connect(self._delete_snapshot_button_clicked)
        self.export_snapshot_button.clicked.connect(self._export_snapshot_button_clicked)
        self.about_snapshot_button.clicked.connect(self._about_snapshot_button_clicked)

        self.import_action.triggered.connect(self._import_action_clicked)
        self.exit_action.triggered.connect(lambda: sys.exit(0))

        self.settings_action.triggered.connect(self._settings_dialog.open_dialog)

        self.uninstalled_apps_snapshot_delete_action.triggered.connect(self._uninstalled_apps_snapshot_delete_action_clicked)
        self.delete_broken_snapshots_action.triggered.connect(self._delete_broken_snapshots_action_clicked)

        self.welcome_dialog_action.triggered.connect(self.welcome_dialog.open_dialog)
        self.view_source_action.triggered.connect(lambda: webbrowser.open("https://codeberg.org/JakobDev/jdFlatpakSnapshot"))
        self.report_bug_action.triggered.connect(lambda: webbrowser.open("https://codeberg.org/JakobDev/jdFlatpakSnapshot/issues"))
        self.translate_action.triggered.connect(lambda: webbrowser.open("https://translate.codeberg.org/projects/jdFlatpakSnapshot"))
        self.donate_action.triggered.connect(lambda: webbrowser.open("https://ko-fi.com/jakobdev"))
        self.about_action.triggered.connect(self._about_dialog.exec)
        self.about_qt_action.triggered.connect(QApplication.instance().aboutQt)

        if self.list_apps.count() == 0:
            QMessageBox.critical(self, QCoreApplication.translate("MainWindow", "No Flatpaks found"), QCoreApplication.translate("MainWindow", "No flatpaks were found on your system. Make sure that some are installed and jdFlatpakSnapshot has the necessary permissions. If the problem persists, please report it. You can access the bug reporting page from the ? menu."))

    def _fill_app_list(self) -> None:
        self.list_apps.clear()

        known_ids = []
        for i in FLATPAK_DIRS:
            self._load_apps(i, known_ids)

        self.list_apps.sortItems(Qt.SortOrder.AscendingOrder)
        self.update_app_list_visible()

    def _load_apps(self, flatpak_path: str, known_ids: list[str]) -> None:
        if not os.path.isdir(flatpak_path):
            return

        if not os.path.isdir(os.path.join(flatpak_path, "app")):
            return

        for i in os.listdir(os.path.join(flatpak_path, "app")):
            app_id = i.removesuffix(".desktop")

            if app_id in known_ids:
                continue

            known_ids.append(app_id)

            name = _get_name_from_desktop_entry(os.path.join(flatpak_path,  "exports", "share" , "applications", i + ".desktop"), app_id, self._env.settings.get("language"))

            icon = None
            if os.path.isfile(os.path.join(flatpak_path, "exports", "share" , "icons", "hicolor", "scalable", "apps", app_id + ".svg")):
                icon = QIcon(os.path.join(flatpak_path, "exports", "share" , "icons", "hicolor", "scalable","apps",  app_id + ".svg"))
            else:
                for size in ("512x512", "256x256", "128x128", "96x96", "64x64", "48x48", "32x32", "24x24", "22x22", "16x16"):
                    if os.path.isfile(os.path.join(flatpak_path, "exports", "share" , "icons", "hicolor", size, "apps",  app_id + ".png")):
                        icon = QIcon(os.path.join(flatpak_path, "exports", "share" , "icons", "hicolor", size, "apps",  app_id + ".png"))

            if icon is None:
                item = QListWidgetItem(self._default_icon, name or app_id)
            else:
                 item = QListWidgetItem(icon, name or app_id)
            item.setData(42, i)
            self.list_apps.addItem(item)

    def _get_selected_snapshot(self) -> Optional["Snapshot"]:
        return self._env.snapshot_collection.get_snapshot_by_id(self.snapshot_list.currentItem().data(42))

    def update_app_list_visible(self) -> None:
        for i in range(self.list_apps.count()):
            item = self.list_apps.item(i)
            app_id = item.data(42)

            if item.text() == app_id and not self._env.settings.get("showSystemApps"):
                item.setHidden(True)
                continue

            if not os.path.isdir(os.path.join(os.path.expanduser("~/.var/app"), app_id)) and not self._env.settings.get("showAppsWithNoData"):
                item.setHidden(True)
                continue

            item.setHidden(False)

        self.list_apps.setCurrentRow(-1)
        self._list_apps_item_changed()

    def _list_apps_item_changed(self) -> None:
        self.create_snapshot_button.setEnabled(self.list_apps.currentRow() != -1)
        self.update_snapshot_list()

    def update_snapshot_list(self) -> None:
        self.snapshot_list.clear()

        self.restore_snapshot_button.setEnabled(False)
        self.rename_snapshot_button.setEnabled(False)
        self.delete_snapshot_button.setEnabled(False)
        self.export_snapshot_button.setEnabled(False)
        self.about_snapshot_button.setEnabled(False)

        if self.list_apps.currentItem() is None:
            return

        if self.list_apps.currentItem().data(42) not in self._env.snapshot_collection.snapshots:
            return

        for i in self._env.snapshot_collection.snapshots[self.list_apps.currentItem().data(42)]:
            if i.is_valid():
                item = QListWidgetItem(i.name)
                item.setData(42, i.id)
                self.snapshot_list.addItem(item)

    def _update_snapshot_buttons_enabled(self) -> None:
        enabled = self.snapshot_list.currentRow() != -1
        self.restore_snapshot_button.setEnabled(enabled)
        self.rename_snapshot_button.setEnabled(enabled)
        self.delete_snapshot_button.setEnabled(enabled)
        self.export_snapshot_button.setEnabled(enabled)
        self.about_snapshot_button.setEnabled(enabled)

    def _import_action_clicked(self) -> None:
        filter = QCoreApplication.translate("MainWindow", "Exported Snapshots") + " (*.flatpaksnapshot);;" +   QCoreApplication.translate("MainWindow", "All Files") + " (*)"
        path = QFileDialog.getOpenFileName(self, filter=filter)[0]

        if path == "":
            return

        import_file(self._env, path, self)

        self.update_snapshot_list()

    def _uninstalled_apps_snapshot_delete_action_clicked(self) -> None:
        if QMessageBox.question(self, QCoreApplication.translate("MainWindow", "Delete Snapshot of uninstalled Apps"), QCoreApplication.translate("MainWindow", "This will delete all Snapshots of apps that are no longer installed. Do you want to continue?")) != QMessageBox.StandardButton.Yes:
           return

        self._env.snapshot_collection.delete_snapshots_of_uninstalled_apps()
        self._env.snapshot_collection.save_snapshots()

        self.update_snapshot_list()

        QMessageBox.information(self, QCoreApplication.translate("MainWindow", "Snapshots deleted"), QCoreApplication.translate("MainWindow", "The Snapshots were successfully deleted"))

    def _delete_broken_snapshots_action_clicked(self) -> None:
        if QMessageBox.question(self, QCoreApplication.translate("MainWindow", "Delete broken Snapshots"), QCoreApplication.translate("MainWindow", "This will delete all broken Snaphots. This might be needed, when a Bug occurs during the creation of a Snaphot or the data is messed up. Do you want to continue?")) != QMessageBox.StandardButton.Yes:
           return

        self._env.snapshot_collection.delete_broken_snapshots()
        self._env.snapshot_collection.save_snapshots()

        self.update_snapshot_list()

        QMessageBox.information(self, QCoreApplication.translate("MainWindow", "Snapshots deleted"), QCoreApplication.translate("MainWindow", "The Snapshots were successfully deleted"))

    def _create_snapshot_button_clicked(self) -> None:
        app_id = self.list_apps.currentItem().data(42)

        if not os.path.isdir(os.path.join(os.path.expanduser("~/.var/app"), app_id)):
            QMessageBox.critical(self, QCoreApplication.translate("MainWindow", "No data"), QCoreApplication.translate("MainWindow", "This Flatpak has no Data"))
            return

        if self._env.flatpak_handler.is_running(app_id) and not self._env.settings.get("allowCreatingWhileRunning"):
            QMessageBox.critical(self, QCoreApplication.translate("MainWindow", "Flatpak running"), QCoreApplication.translate("MainWindow", "This Flatpak ts currently running. You can't restore the Snapshot of a Flatpak while it's running."))
            return

        commit = self._env.flatpak_handler.get_installed_commit(app_id)
        if not commit:
            QMessageBox.critical(self, QCoreApplication.translate("MainWindow", "Could not get Commit"), QCoreApplication.translate("MainWindow", "Could not get the commit for this Flatpak. You still can craete a Snapshot, but you will not know, to which Version it belongs."))

        name, ok = QInputDialog.getText(self, QCoreApplication.translate("MainWindow", "Enter Name"), QCoreApplication.translate("MainWindow", "Please enter a Name for your Snapshot"))

        if not ok or name == "":
            return

        if self._env.snapshot_collection.do_snapshot_name_exists(app_id, name):
            QMessageBox.critical(self, QCoreApplication.translate("MainWindow", "Name exists"), QCoreApplication.translate("MainWindow", "This Name already exists"))
            return

        new_snapshot = self._env.snapshot_collection.generate_new_snapshot()
        snapshot_path = os.path.join(self._env.data_dir, "snapshots", app_id, new_snapshot.id + ".tar")
        new_snapshot.app_id = app_id

        comp_method, ok, = QInputDialog.getItem(self, QCoreApplication.translate("MainWindow", "Compression method"), QCoreApplication.translate("MainWindow", "Please choose a compression method"), [i.name for i in COMPRESSION_METHODS], editable=False)

        if not ok:
            return

        for comp in COMPRESSION_METHODS:
            if comp.name == comp_method:
                compression_method_data = comp
                break

        save_path = snapshot_path + compression_method_data.suffix

        new_snapshot.name = name
        new_snapshot.filename = os.path.basename(save_path)
        new_snapshot.timestamp = int(datetime.datetime.now().timestamp())
        new_snapshot.commit = commit

        self._progress_dialog.create_tar_archive(new_snapshot)

    def _restore_snapshot_button_clicked(self) -> None:
        current_snapshot = self._get_selected_snapshot()

        if self._env.flatpak_handler.is_running(current_snapshot.app_id) and not self._env.settings.get("allowRestoringWhileRunning"):
            QMessageBox.critical(self, QCoreApplication.translate("MainWindow", "Flatpak running"), QCoreApplication.translate("MainWindow", "This Flatpak ts currently running. You can't restore the Snapshot of a Flatpak while it's running."))
            return

        if QMessageBox.question(self, QCoreApplication.translate("MainWindow", "Restore Snapshot"), QCoreApplication.translate("MainWindow", "Are you sure you want to restore this Snapshot? This will overwrite all Data of this Flatpak.")) != QMessageBox.StandardButton.Yes:
            return

        data_dir = os.path.join(os.path.expanduser("~/.var/app"), current_snapshot.app_id)

        try:
            shutil.rmtree(data_dir)
        except FileNotFoundError:
            pass
        except Exception:
            QMessageBox.critical(self, QCoreApplication.translate("MainWindow", "Error"), QCoreApplication.translate("MainWindow", "An error occurred while deleting {{path}}").replace("{{path}}", data_dir))
            return

        self._progress_dialog.extract_tar_archive(current_snapshot)

    def _rename_snapshot_button_clicked(self) -> None:
        name, ok = QInputDialog.getText(self, QCoreApplication.translate("MainWindow", "New name"), QCoreApplication.translate("MainWindow", "Please enter a new name"))

        if not ok or name == "":
            return

        current_snapshot = self._get_selected_snapshot()

        if self._env.snapshot_collection.do_snapshot_name_exists(current_snapshot.app_id,name):
            QMessageBox.critical(self, QCoreApplication.translate("MainWindow", "Name exists"), QCoreApplication.translate("MainWindow", "This name already exists"))
            return

        current_snapshot.name = name

        self.update_snapshot_list()

    def _delete_snapshot_button_clicked(self) -> None:
        if QMessageBox.question(self, QCoreApplication.translate("MainWindow", "Delete snapshot"), QCoreApplication.translate("MainWindow", "Are you sure you want to delete this snapshot?")) != QMessageBox.StandardButton.Yes:
           return

        current_snapshot = self._get_selected_snapshot()

        self._env.snapshot_collection.delete_snapshot(current_snapshot)

        self._env.snapshot_collection.save_snapshots()
        self.update_snapshot_list()

        QMessageBox.information(self, QCoreApplication.translate("MainWindow", "Snapshot deleted"), QCoreApplication.translate("MainWindow", "The snapshot was successfully deleted"))

    def _export_snapshot_button_clicked(self) -> None:
        filter = QCoreApplication.translate("MainWindow", "Exported Snapshots") + " (*.flatpaksnapshot);;" +   QCoreApplication.translate("MainWindow", "All Files") + " (*)"
        path = QFileDialog.getSaveFileName(self, filter=filter)[0]

        if path == "":
            return

        export_single_snapshot(self._env, self._get_selected_snapshot(), path, self)

    def _about_snapshot_button_clicked(self) -> None:
        snapshot = self._get_selected_snapshot()

        text =  QCoreApplication.translate("MainWindow", "Compression: {{compression}}").replace("{{compression}}", snapshot.get_compression_method().name) + "<br>"
        text += QCoreApplication.translate("MainWindow", "Size on disk: {{size}}").replace("{{size}}", human_readable_size(os.path.getsize(os.path.join(self._env.data_dir, "snapshots", snapshot.app_id, snapshot.filename)))) + "<br>"
        text += QCoreApplication.translate("MainWindow", "Created on: {{datetime}}").replace("{{datetime}}", format_datetime(datetime.datetime.fromtimestamp(snapshot.timestamp), self._env.settings.get("datetimeFormat"))) + "<br>"
        text += QCoreApplication.translate("MainWindow", "Commit: {{commit}}").replace("{{commit}}", snapshot.commit or QCoreApplication.translate("MainWindow", "Unknown"))

        QMessageBox.information(self, QCoreApplication.translate("MainWindow", "About {{name}}").replace("{{name}}", self.snapshot_list.currentItem().text()), text)
