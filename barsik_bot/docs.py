import json
from os import PathLike
from pathlib import Path
from typing import Optional, Union

import disnake


class Docs:
    def __init__(self, **kwargs) -> None:
        self._id: str = kwargs.pop("id")
        self._type: str = kwargs.pop("type")

    @property
    def id(self) -> str:
        return self._id

    @property
    def type(self) -> str:
        return self._type

    def __str__(self) -> str:
        return self.id

    def __repr__(self) -> str:
        return "<%s id=%s type=%s>" % (
            self.__class__.__name__,
            repr(self.id),
            repr(self.type),
        )


class SlashCommandOptionDocs:
    def __init__(self, **kwargs) -> None:
        self._name: str = kwargs.pop("name")
        self._description: str = kwargs.pop("description", "...")
        self._required: bool = kwargs.pop("required", False)

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def required(self) -> bool:
        return self._required

    def __bool__(self) -> bool:
        return self.required

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return "<%s name=%s description=%s required=%s>" % (
            self.__class__.__name__,
            repr(self.name),
            repr(self.description),
            self.required,
        )


class SlashCommandDocs(Docs):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._name: Optional[str] = kwargs.get("name")
        self._description: Optional[str] = kwargs.get("description")
        self._options: Optional[list[dict]] = kwargs.get("options")
        self._permissions: Optional[list[str]] = kwargs.get("permissions")

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def options(self) -> Optional[list[SlashCommandOptionDocs]]:
        return [
            SlashCommandOptionDocs(**option) for option in self._options if option
        ] or None

    @property
    def permissions(self) -> Optional[list[str]]:
        return (
            [
                permission
                for permission in self._permissions
                if permission in disnake.Permissions.VALID_FLAGS.keys()
            ]
            if self._permissions
            else None
        )

    def __str__(self) -> str:
        return f"/{self.name}"

    def __len__(self) -> int:
        return len(self.options)

    def __repr__(self) -> str:
        return "<%s id=%s name=%s description=%s options=%s>" % (
            self.__class__.__name__,
            repr(self.id),
            repr(self.name),
            repr(self.description),
            self.options,
        )


class DocsNotFound(Exception):
    def __init__(self, docs: str) -> None:
        self.docs = docs

    def __str__(self) -> str:
        return f"Docs {self.docs!r} not found!"


default_data_types = {"slash-command": SlashCommandDocs}


class DockLoader:
    def __init__(self) -> None:
        self._types: dict[str, Docs] = default_data_types
        self._data: list[Docs] = []

    def set_types(self, types: dict[str, Docs]):
        self._types = types

    def load(self, path: Union[str, PathLike, Path]) -> None:
        path = Path(path) if not isinstance(path, Path) else path
        if not path.exists() and not path.is_file():
            raise FileNotFoundError(path)
        with path.open(encoding="utf-8") as file:
            load: list[dict] = json.load(file)
        for item in load:
            if docs_type := item.get("type"):
                self._data.append(self.types.get(docs_type, Docs)(**item))

    def get(self, docs_id: str, type_id: Docs = Docs) -> Optional[Docs]:
        for item in self.data:
            if item.id == docs_id and item.type == type_id:
                return item

    @property
    def data(self) -> list[Docs]:
        return self._data

    @property
    def types(self) -> dict[str, Docs]:
        return self._types
