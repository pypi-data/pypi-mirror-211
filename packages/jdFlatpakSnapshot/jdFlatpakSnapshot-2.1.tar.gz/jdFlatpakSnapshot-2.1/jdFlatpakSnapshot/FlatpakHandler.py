from typing import Optional, TYPE_CHECKING
from .Functions import is_run_as_flatpak
import subprocess


if TYPE_CHECKING:
    from .Environment import Environment


class FlatpakHandler:
    def __init__(self, env: "Environment") -> None:
        self._env = env

    def _get_flatpak_command(self) -> list[str]:
        if is_run_as_flatpak():
            return ["flatpak-spawn", "--host", self._env.settings.get("flatpakCommand")]
        else:
            return [self._env.settings.get("flatpakCommand")]


    def get_installed_commit(self, app_id: str) -> Optional[str]:
        """
        Returns the commit of the given Flatpak App
        """
        try:
            return subprocess.run(self._get_flatpak_command() + ["info", "-c", app_id], capture_output=True, check=True).stdout.decode("utf-8").strip()
        except Exception:
            return None


    def is_running(self, app_id: str) -> bool:
        """
        Checks if the given App is running
        """
        try:
            for app in subprocess.run(self._get_flatpak_command() + ["ps", "--columns=application"], capture_output=True, check=True).stdout.decode("utf-8").splitlines():
                if app == app_id:
                    return True
            return False
        except Exception:
            return False
