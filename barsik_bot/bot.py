from datetime import datetime
from pathlib import Path
from typing import Optional

from disnake import Client
from disnake.ext import commands
from disnake.ext.commands import InvokableSlashCommand

from .config import Config
from .docs import DockLoader
from .locale import BotLocalizationStore
from .errors import ErrorHandler


class BarsikBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(
            command_prefix=commands.when_mentioned, reload=True, *args, **kwargs
        )
        self.i18n = BotLocalizationStore()
        self.docs = DockLoader()
        self.error_handler = ErrorHandler(self)
        self._start_up = datetime.now()
        self._config: Config = Config()

    @property
    def start_up(self) -> datetime:
        return self._start_up

    @property
    def config(self) -> Config:
        return self._config

    def load_extensions(self, **kwargs) -> None:
        for path in Path(self.config.get("files").get("extensions")).glob("**/*.py"):
            self.load_extension(".".join(path.parts)[: -len(path.suffix)])

    def run(self, token: Optional[str] = None) -> None:
        super().run(token or self.config.get("token"))

    def add_slash_command(self, slash_command: InvokableSlashCommand) -> None:
        if not isinstance(self, Client):
            raise NotImplementedError(
                "This method is only usable in disnake.Client subclasses"
            )

        if not isinstance(slash_command, InvokableSlashCommand):
            raise TypeError(
                "The slash_command passed must be an instance of InvokableSlashCommand"
            )

        if slash_command.name not in self.all_slash_commands:
            slash_command.body.localize(self.i18n)
            self.all_slash_commands[slash_command.name] = slash_command
