import json
from os import PathLike
from pathlib import Path
from typing import Final, Optional, overload, Union

default_config: Final[dict] = {
    "token": "<not specified>",
    "owners": [],
    "description": "<not specified>",
    "log-format": (
        "<fg #1E5945>[</fg #1E5945><fg #47A76A>{time:HH:mm:ss DD.MM.YYYY}</fg #47A76A><fg #1E5945>]</fg #1E5945> "
        "<fg #1E5945>[</fg #1E5945><level>{level: <8}</level><fg #1E5945>]</fg #1E5945> {message}"
    ),
    "files": {
        "locals": "./src/locales/",
        "docs": "./src/bot-docs.json",
        "extensions": "./barsik_bot/extensions/",
        "logs": "./src/logs/logs.log",
    },
}


class Config:
    def __init__(self):
        self._data: dict = {}
        self._default: Optional[dict] = default_config
        self._path: Path = None

    @property
    def default(self) -> Optional[dict]:
        return self._default

    def set_default(self, data: dict) -> None:
        self._default = data

    @overload
    def get(self) -> dict:
        ...

    @overload
    def get(self, key: str) -> Optional[Union[str, dict]]:
        ...

    def get(self, key: Optional[str] = None) -> Union[dict, Optional[str]]:
        if key is not None:
            data = self._data
            for key in key.split("."):
                if not isinstance(data, dict):
                    break
                if key in data:
                    data = data.get(key)
            return data
        return self._data

    @overload
    def load(self) -> None:
        ...

    def load(self, path: Union[str, PathLike, Path] = "./config.json") -> bool:
        path = Path(path) if not isinstance(path, Path) else path
        if not path.exists() and not path.is_file():
            return False
        with path.open(encoding="utf-8") as file:
            load: dict = json.load(file)
        self._data = load
        self._path = path
        return True

    @overload
    def generate(self) -> None:
        ...

    def generate(self, path: Union[str, PathLike, Path] = "./config.json") -> None:
        path = Path(path) if not isinstance(path, Path) else path
        with path.open(mode="x") as file:
            json.dump(self._default, file, indent=4)
        self._path = path

    def __bool__(self) -> bool:
        return len(self._data.keys()) == 0
