import toml
from pathlib import Path
from typing import Final, Any

config_file: Final[str] = "./bot-config.toml"


class ConfigFileNotFound(FileNotFoundError):
    def __int__(self):
        super().__init__(f'Config: "{config_file}" not found!')


class BotConfig:
    @staticmethod
    def load() -> dict[str, Any]:
        config = Path(config_file)
        if config.exists():
            with config.open() as file:
                return toml.load(file)["bot"]["main"]
        else:
            raise ConfigFileNotFound
