from typing import Optional, TYPE_CHECKING
from .Functions import is_flatpak_installed
from .Snapshot import Snapshot
import uuid
import json
import sys
import os


if TYPE_CHECKING:
    from .Environment import Environment


class SnapshotCollection:
    def __init__(self, env: "Environment") -> None:
        self._env = env

        self.snapshots: dict[str, Snapshot] = {}

    def load_snapshots(self) -> None:
        try:
            with open(os.path.join(self._env.data_dir, "snapshots.json"), "r", encoding="utf-8") as f:
                for app_id, snapshot_list in json.load(f).items():
                    self.snapshots[app_id] = []
                    for single_snapshot in snapshot_list:
                        snapshot = Snapshot.from_dict(self._env, single_snapshot)
                        snapshot.app_id = app_id
                        self.snapshots[app_id].append(snapshot)
        except FileNotFoundError:
            pass
        except Exception:
            print("Error opening " + os.path.join(self.data_dir, "snapshots.json"), file=sys.stderr)

    def save_snapshots(self) -> None:
        save_data = {}

        for app_id, snapshot_list in self.snapshots.items():
            save_data[app_id] = []
            for i in snapshot_list:
                save_data[app_id].append(i.to_dict())

        with open(os.path.join(self._env.data_dir, "snapshots.json"), "w", encoding="utf-8") as f:
            json.dump(save_data, f, ensure_ascii=False, indent=4)

    def get_snapshot_by_id(self, snapshot_id: str) -> Optional[Snapshot]:
        for snapshot_list in self.snapshots.values():
            for single_snapshot in snapshot_list:
                if single_snapshot.id == snapshot_id:
                    return single_snapshot
        return None

    def delete_snapshot(self,  current_snapshot: Snapshot) -> None:
        try:
            os.remove(current_snapshot.get_full_tar_path())
        except Exception:
            print(current_snapshot.get_full_tar_path() + " could not be removed", file=sys.stderr)

        index = self.snapshots[current_snapshot.app_id].index(current_snapshot)
        del self.snapshots[current_snapshot.app_id][index]

        if len(self.snapshots[current_snapshot.app_id]) == 0:
            del self.snapshots[current_snapshot.app_id]

    def do_snapshot_name_exists(self, app_id, name: str) -> bool:
        for single_snapshot in self.snapshots.get(app_id, []):
            if single_snapshot.name.lower() == name.lower():
                return True
        return False

    def generate_new_snapshot(self) -> Snapshot:
        while True:
            current_id = str(uuid.uuid4())

            if self.get_snapshot_by_id(current_id) is None:
                new_snapshot = Snapshot(self._env)
                new_snapshot.id = current_id
                return new_snapshot

    def add_snapshot(self, new_snapshot: Snapshot) -> None:
        if new_snapshot.app_id not in self.snapshots:
            self.snapshots[new_snapshot.app_id] = [new_snapshot]
        else:
            self.snapshots[new_snapshot.app_id].append(new_snapshot)

    def get_snapshot_list(self) -> list[Snapshot]:
        "Returns all Snapshots as List"
        full_snapshot_list = []
        for app_snapshot_list in self.snapshots.values():
            full_snapshot_list += app_snapshot_list
        return full_snapshot_list

    def delete_snapshots_of_uninstalled_apps(self) -> None:
        "Deletes all Snapshots, that belongs to Apps that are no longer installed"
        for app_id, snapshot_list in self.snapshots.items():
            if not is_flatpak_installed(app_id):
                for single_snapshot in snapshot_list:
                    self.delete_snapshot(single_snapshot)

    def delete_broken_snapshots(self) -> None:
        "Deletes all Snapshots that are broken"
        for single_snapshot in self.get_snapshot_list():
            if not single_snapshot.is_valid():
                self.delete_snapshot(single_snapshot)
