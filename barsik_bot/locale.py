import json

from os import PathLike
from pathlib import Path
from typing import Union, Optional
from disnake import LocalizationProtocol, Locale


class BotLocalizationStore(LocalizationProtocol):
    def __init__(self, default: Locale = Locale.en_US) -> None:
        self.default: Locale = default
        self.data: dict[str, dict[str, str]] = {}

    def get(
        self, key: str, locale: Optional[Locale] = None, *args, **kwargs
    ) -> Union[dict[str, str], str]:
        locale_data = {}
        for loc, data in self.data.items():
            locale_data[loc] = data.get(key, key)
        return (
            locale_data
            if locale is None
            else locale_data.get(locale.value, key).format(*args, **kwargs)
        )

    def load(self, path: Union[str, PathLike]) -> None:
        path = Path(path)
        for path in path.glob("*.json"):
            if locale := Locale.__members__.get(path.stem):
                with path.open(encoding="utf-8") as file:
                    load: dict = json.load(file)
                self.data[locale.value] = load or {}
