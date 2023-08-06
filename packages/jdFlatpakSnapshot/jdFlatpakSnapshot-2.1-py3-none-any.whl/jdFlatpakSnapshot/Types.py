from typing import Optional, TypedDict


class ExportedFileManifest(TypedDict):
    version: int
    app_version: str
    type: str
    app_id: str
