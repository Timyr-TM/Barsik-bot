from typing import Optional, Union

import disnake
from disnake.ext import commands

from barsik_bot import BarsikBot, Docs, DocsNotFound, ErrorEmbed
from barsik_bot.embeds import docs_to_embed


class HelpCommand(commands.InvokableSlashCommand):
    def __init__(self) -> None:
        super().__init__(
            func=self.command_callback,
            name="help",
            description=disnake.Localized(key="slash_command.help"),
        )

    @staticmethod
    async def command_autocomplete(
        inter: disnake.ApplicationCommandInteraction, data: str
    ) -> Optional[list[Union[str, disnake.OptionChoice]]]:
        bot: BarsikBot = inter.bot
        options: list[disnake.OptionChoice] = []
        for doc in bot.docs.data:
            choice = disnake.OptionChoice(name=str(doc), value=doc.id)
            if len(options) > 25:
                break
            if len(data) == 0:
                options.append(choice)
            elif data and data in str(doc):
                options.append(choice)
        return options

    @staticmethod
    async def docs_converter(
        inter: disnake.ApplicationCommandInteraction, data: str
    ) -> Optional[Docs]:
        bot: BarsikBot = inter.bot
        for doc in bot.docs.data:
            if doc.id == data:
                return doc
        raise DocsNotFound(data)

    async def command_callback(
        self,
        inter: disnake.ApplicationCommandInteraction,
        docs: Optional[Docs] = commands.Param(
            name="docs",
            autocomplete=command_autocomplete,
            converter=docs_converter,
            description=disnake.Localized(key="slash_command.help.option.docs"),
        ),
    ) -> None:
        await inter.send(embed=docs_to_embed(docs, inter.locale, inter.bot))


class DocsNotFoundErrorEmbed(ErrorEmbed[DocsNotFound]):
    def __init__(
        self, inter: disnake.ApplicationCommandInteraction, error: DocsNotFound
    ):
        super().__init__(inter, error)
        self.description = inter.bot.i18n.get(
            "docs_not_found", inter.locale, docs=error.docs
        )


def setup(bot: BarsikBot) -> None:
    bot.add_slash_command(HelpCommand())
    bot.error_handler.add_error(DocsNotFound, DocsNotFoundErrorEmbed)
