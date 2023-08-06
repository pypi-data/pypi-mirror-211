from .Functions import human_readable_size, format_datetime, extract_file_from_zip, is_flatpak_installed
from PyQt6.QtWidgets import QWidget, QMessageBox, QInputDialog
from PyQt6.QtCore import QCoreApplication
from .Types import ExportedFileManifest
from typing import TYPE_CHECKING
from .Snapshot import Snapshot
import traceback
import datetime
import zipfile
import json
import sys
import os


if TYPE_CHECKING:
    from .Environment import Environment


def _import_single_snapshot(env: "Environment", app_id: str, parent: QWidget, zf: zipfile.ZipFile):
    new_snapshot = env.snapshot_collection.generate_new_snapshot()
    new_snapshot.app_id = app_id

    with zf.open("metadata.json", "r") as f:
        new_snapshot.load_dict(json.load(f))

    new_snapshot.regenerate_filename()
    file_name = "data.tar" + new_snapshot.get_compression_method().suffix

    text = QCoreApplication.translate("ImportExport", "This includes the following Snapshot:") + "<br>"
    text += QCoreApplication.translate("ImportExport", "App: {{app}}").replace("{{app}}", new_snapshot.app_id) + "<br>"
    text += QCoreApplication.translate("ImportExport", "Name: {{name}}").replace("{{name}}", new_snapshot.name) + "<br>"
    text += QCoreApplication.translate("ImportExport", "Compression: {{compression}}").replace("{{compression}}", new_snapshot.get_compression_method().name) + "<br>"
    text += QCoreApplication.translate("ImportExport", "Size on disk: {{size}}").replace("{{size}}", human_readable_size(zf.getinfo(file_name).file_size)) + "<br>"
    text += QCoreApplication.translate("ImportExport", "Created on: {{datetime}}").replace("{{datetime}}", format_datetime(datetime.datetime.fromtimestamp(new_snapshot.timestamp), env.settings.get("datetimeFormat"))) + "<br><br>"
    text += QCoreApplication.translate("ImportExport", "Do you want to import it?")

    if QMessageBox.question(parent, QCoreApplication.translate("ImportExport", "Import"), text, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) != QMessageBox.StandardButton.Yes:
        return

    if not is_flatpak_installed(new_snapshot.app_id):
        if QMessageBox.question(parent, QCoreApplication.translate("ImportExport", "App not installed"), QCoreApplication.translate("ImportExport", "It looks like {{app}} is not installed. Are you really want to import the data?").replace("{{app}}", new_snapshot.app_id), QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) != QMessageBox.StandardButton.Yes:
            return

    if env.snapshot_collection.do_snapshot_name_exists(new_snapshot.app_id, new_snapshot.name):
        while True:
            new_name = QInputDialog.getText(parent, QCoreApplication.translate("ImportExport", "New name"), QCoreApplication.translate("ImportExport", "There is already a Snapshot with this Name for this App. Please enter a new one."))[0].strip()

            if new_name == "":
                return

            if env.snapshot_collection.do_snapshot_name_exists(new_snapshot.app_id, new_name):
                QMessageBox.information(parent,  QCoreApplication.translate("ImportExport", "Name exists"),  QCoreApplication.translate("ImportExport", "This Name also exists. Please enter a new one."))
            else:
                new_snapshot.name = new_name
                break

    extract_file_from_zip(zf, file_name, new_snapshot.get_full_tar_path())

    env.snapshot_collection.add_snapshot(new_snapshot)
    env.snapshot_collection.save_snapshots()


def import_file(env: "Environment", path: str, parent: QWidget) -> None:
    try:
        zf = zipfile.ZipFile(path, "r")

        with zf.open("manifest.json", "r") as f:
            manifest: ExportedFileManifest = json.loads(f.read())

        if manifest["version"] != 1 or manifest["type"] != "single_snapshot":
            QMessageBox.critical(parent, QCoreApplication("ImportExport", "Unsuported version", "This Export was created by a newer version of jdFlatpakSnapshot. You need to update to use it."))
            return

        _import_single_snapshot(env, manifest["app_id"], parent, zf)
    except Exception:
        print(traceback.format_exc(),end="",file=sys.stderr)
        QMessageBox.critical(parent,QCoreApplication.translate("ImportExport", "Error"), QCoreApplication.translate("ImportExport", "An error occurred during import. Maybe the File is not valid."))
    finally:
        try:
            zf.close()
        except Exception:
            pass


def export_single_snapshot(env: "Environment", current_snapshot: Snapshot, path: str, parent: QWidget) -> None:
    try:
        with zipfile.ZipFile(path, "w") as zf:
            zf.write(current_snapshot.get_full_tar_path(), "data." + current_snapshot.filename.split(".", 1)[1])
            zf.writestr("metadata.json", json.dumps(current_snapshot.to_dict(), ensure_ascii=False, indent=4))
            zf.writestr("manifest.json", json.dumps({
                "version": 1,
                "app_version": env.version,
                "type": "single_snapshot",
                "app_id": current_snapshot.app_id
            }, ensure_ascii=False, indent=4))
    except Exception:
        try:
            os.remove(path)
        except Exception:
            pass

        print(traceback.format_exc(),end="",file=sys.stderr)
        QMessageBox.critical(parent, QCoreApplication.translate("ImportExport", "Export failed"), QCoreApplication.translate("ImportExport", "Cound not export {{name}}"). replace("{{name}}", current_snapshot.name))