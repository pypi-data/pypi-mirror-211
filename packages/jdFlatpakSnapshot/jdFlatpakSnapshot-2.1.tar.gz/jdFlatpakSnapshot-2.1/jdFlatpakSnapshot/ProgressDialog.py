from PyQt6.QtCore import QCoreApplication, QThread, pyqtSignal
from .ui_compiled.ProgressDialog import Ui_ProgressDialog
from .Functions import list_files_recursive
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QCloseEvent
from typing import TYPE_CHECKING
import tarfile
import os


if TYPE_CHECKING:
    from .Environment import Environment
    from .Snapshot import Snapshot


class CompressThread(QThread):
    set_text =  pyqtSignal("QString")
    set_value = pyqtSignal("int")
    set_maximum = pyqtSignal("int")
    creation_finished = pyqtSignal()
    extraction_finished = pyqtSignal()

    def setup_compress(self, current_snapshot: "Snapshot") -> None:
        self._current_snapshot = current_snapshot
        self._mode = "create"

    def setup_extract(self, current_snapshot: "Snapshot") -> None:
        self._current_snapshot = current_snapshot
        self._mode = "extract"

    def _create_snapshot(self) -> None:
        self.set_text.emit(QCoreApplication.translate("ProgressDialog", "Scanning files. Please wait..."))

        source_dir = os.path.join(os.path.expanduser("~/.var/app"), self._current_snapshot.app_id)

        file_list = list_files_recursive(source_dir)
        self.set_maximum.emit(len(file_list))

        tf = tarfile.open(self._current_snapshot.get_full_tar_path(), "x:" + self._current_snapshot.get_compression_method().mode)

        for count, i in enumerate(file_list):
            self.set_text.emit(QCoreApplication.translate("ProgressDialog", "Compressing {{path}}").replace("{{path}}", i))
            self.set_value.emit(count)
            tf.add(os.path.join(source_dir, i), arcname=i)
        tf.close()

        self.creation_finished.emit()

    def _extract_snapshot(self) -> None:
        tf = tarfile.open(self._current_snapshot.get_full_tar_path(), "r:" + self._current_snapshot.get_compression_method().mode)

        out_dir = os.path.join(os.path.expanduser("~/.var/app"), self._current_snapshot.app_id)

        name_list = tf.getnames()
        self.set_maximum.emit(len(name_list))

        for count, i in enumerate(name_list):
            self.set_text.emit(QCoreApplication.translate("ProgressDialog", "Extracting {{path}}").replace("{{path}}", i))
            self.set_value.emit(count)
            tf.extract(i, out_dir)
        tf.close()

        self.extraction_finished.emit()

    def run(self):
        if self._mode == "create":
            self._create_snapshot()
        elif self._mode == "extract":
            self._extract_snapshot()


class ProgressDialog(QDialog, Ui_ProgressDialog):
    def __init__(self, env: "Environment", main_window) -> None:
        super().__init__()

        self.setupUi(self)

        self._env = env
        self._finished = False
        self._main_window = main_window

        self.setModal(True)

        self._progress_thread = CompressThread()
        self._progress_thread.set_text.connect(lambda text: self.progress_label.setText(text))
        self._progress_thread.set_value.connect(lambda value: self.progress_bar.setValue(value))
        self._progress_thread.set_maximum.connect(lambda maximum: self.progress_bar.setMaximum(maximum))
        self._progress_thread.creation_finished.connect(self._creation_finished)
        self._progress_thread.extraction_finished.connect(self._extract_finished)

        self.cancel_button.clicked.connect(self.close)

    def create_tar_archive(self, currrent_snapshot: "Snapshot") -> None:
        self.show()

        try:
            os.makedirs(os.path.dirname(currrent_snapshot.get_full_tar_path()))
        except Exception:
            pass

        self._current_snapshot = currrent_snapshot
        self._finished = False

        self._progress_thread.setup_compress(currrent_snapshot)
        self._progress_thread.start()

    def _creation_finished(self) -> None:
        self._env.snapshot_collection.add_snapshot(self._current_snapshot)

        self._env.snapshot_collection.save_snapshots()
        self._main_window.update_snapshot_list()

        self._finished = True
        self.close()

    def extract_tar_archive(self, current_snapshot: "Snapshot") -> None:
        self.show()

        out_dir = os.path.join(os.path.expanduser("~/.var/app"), current_snapshot.app_id)
        os.makedirs(out_dir)

        self._current_snapshot = current_snapshot
        self._finished = False

        self._progress_thread.setup_extract(current_snapshot)
        self._progress_thread.start()

    def _extract_finished(self) -> None:
        self._finished = True
        self.close()

    def closeEvent(self, event: QCloseEvent) -> None:
        if not self._finished:
            self._progress_thread.terminate()
            if self._current_snapshot is not None:
                try:
                    os.remove(self._current_snapshot.get_full_tar_path())
                except Exception:
                    pass

        event.accept()
