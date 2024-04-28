from disnake import Embed, Event, ApplicationCommandInteraction, Color
from disnake.ext.commands import CommandError, Bot
from loguru import logger
from typing import Optional, TypeVar, Generic


T = TypeVar("T")


class ErrorEmbed(Embed, Generic[T]):
    def __init__(self, inter: ApplicationCommandInteraction, error: T) -> None:
        super().__init__(
            title=inter.bot.i18n.get("error.title", inter.locale), color=Color.red()
        )
        self._inter = inter
        self._error = error

    @property
    def inter(self) -> ApplicationCommandInteraction:
        return self._inter

    @property
    def error(self) -> T:
        return self._error


class UnknownErrorEmbed(ErrorEmbed):
    def __init__(self, inter: ApplicationCommandInteraction, error: CommandError):
        super().__init__(inter, error)
        self.description = inter.bot.i18n.get("error.unknown", inter.locale)


class ErrorHandler:
    def __init__(self, bot: Bot) -> None:
        self._bot: Bot = bot
        self.errors: dict[type[CommandError], type[ErrorEmbed[CommandError]]] = {}
        self.events: list[Event] = [
            Event.slash_command_error,
            Event.user_command_error,
            Event.message_command_error,
        ]

    @property
    def bot(self) -> Bot:
        return self._bot

    def add_error(
        self, error: type[CommandError], embed: type[ErrorEmbed[CommandError]]
    ) -> None:
        self.errors[error] = embed

    def get_embed(
        self, error: type[CommandError]
    ) -> Optional[type[ErrorEmbed[CommandError]]]:
        return self.errors.get(error)

    def remove_embed(self, error: type[CommandError]) -> bool:
        if self.errors.get(error) is not None:
            del self.errors[error]
            return True
        return False

    async def callback(
        self, inter: ApplicationCommandInteraction, error: CommandError
    ) -> None:
        if (embed := self.get_embed(type(error.original))) is None:
            logger.error(error)
        return await inter.send(
            embed=(embed or UnknownErrorEmbed)(inter, error.original),
            ephemeral=inter.guild is not None,
        )

    def load(self) -> None:
        for event in self.events:
            self.bot.add_listener(self.callback, event)
