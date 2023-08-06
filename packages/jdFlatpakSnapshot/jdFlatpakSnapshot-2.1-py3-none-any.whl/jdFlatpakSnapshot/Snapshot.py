from PyQt6.QtCore import QObject
from .Constants import CompressionTuple, COMPRESSION_METHODS
from typing import TYPE_CHECKING
import uuid
import os


if TYPE_CHECKING:
    from .Environment import Environment


class Snapshot(QObject):
    def __init__(self, env: "Environment") -> None:
        super().__init__()

        self._env = env

        self.name: str = ""
        self.id = str(uuid.uuid4())
        self.filename: str = ""
        self.timestamp: int = 0
        self.commit: str | None = None
        self.app_id: str = ""

    def load_dict(self, snapshot_dict: dict) -> None:
        self.name = snapshot_dict["name"]
        self.filename = snapshot_dict["filename"]
        self.timestamp = snapshot_dict["timestamp"]
        self.commit = snapshot_dict.get("commit")

    @classmethod
    def from_dict(cls: "Snapshot", env: "Environment", snapshot_dict: dict) -> "Snapshot":
        snapshot = cls(env)

        snapshot.load_dict(snapshot_dict)
        snapshot.id = snapshot_dict.get("id", snapshot_dict["filename"][:36])

        return snapshot

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "filename": self.filename,
            "timestamp": self.timestamp,
            "commit": self.commit
        }

    def regenerate_filename(self) -> None:
        self.filename = self.id + ".tar" + self.get_compression_method().suffix

    def get_full_tar_path(self) -> str:
        return os.path.join(self._env.data_dir, "snapshots", self.app_id, self.filename)

    def is_valid(self) -> bool:
        return os.path.isfile(self.get_full_tar_path())

    def get_compression_method(self) -> CompressionTuple:
        for method in reversed(COMPRESSION_METHODS):
            if self.filename.endswith(method.suffix):
                return method

    def __repr__(self) -> str:
        return f"<Snapshot id='{self.id}' name='{self.name}'>"
