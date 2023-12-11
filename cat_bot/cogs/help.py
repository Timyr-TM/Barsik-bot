import json
from typing import NoReturn, Optional
import disnake

from disnake.ext import commands
from ..utils.bot_locale import BotLocal


class HelpCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @staticmethod
    async def help_autocomplete(
        inter: disnake.ApplicationCommandInteraction, data: str
    ) -> list[disnake.OptionChoice]:
        options: list[disnake.OptionChoice] = []
        with open(r"./src/command-info.json", encoding="utf-8") as file:
            load: dict = json.load(file) or {}
        for key, value in load.items():
            if len(options) < 25 and data in value.get("name"):
                options.append(
                    disnake.OptionChoice(name=value.get("name") or "...", value=key)
                )
        return options

    @staticmethod
    async def help_converter(
        inter: disnake.ApplicationCommandInteraction, data: str
    ) -> Optional[dict]:
        with open(r"./src/command-info.json", encoding="utf-8") as file:
            load: dict = json.load(file).get(data)
        return load

    @commands.slash_command(
        name="help", description=BotLocal("slash_command.help").get_localized
    )
    async def help_command(
        self,
        inter: disnake.ApplicationCommandInteraction,
        command: dict = commands.Param(
            name="command",
            description=BotLocal("slash_command.help.options.command").get_localized,
            autocomplete=help_autocomplete,
            converter=help_converter,
        ),
    ) -> NoReturn:
        embed = disnake.Embed(
            title=(
                BotLocal("slash_command.help.main_embed.title")
                .get(inter.locale)
                .format(command=f"`/{command.get('name')}`")
            ),
            url=command.get("link"),
            color=disnake.Color.blurple(),
            description=(
                f"{BotLocal(command.get('description')).get(inter.locale)}\n"
                if command.get("description")
                else None
            ),
        )
        if command.get("options"):
            options = ""
            for option in command.get("options"):
                required: str = (
                    f" *({BotLocal('slash_command.help.main_embed.options.required').get(inter.locale)})*"
                    if option.get("required")
                    else ""
                )
                options += (
                    f"- **{option.get('name')}**{required}\n"
                    f" {BotLocal(option.get('description')).get(inter.locale)}\n"
                )
            embed.add_field(
                name=BotLocal('slash_command.help.main_embed.options').get(inter.locale),
                value=options,
                inline = False
            )
        
        if command.get("permissions"):
            permissions = ""
            for permission in command.get("permissions"):
                local = BotLocal(f"permission.{permission}").get(inter.locale)
                permissions += f"- {local}\n"
            embed.add_field(
                name = BotLocal('slash_command.help.main_embed.permissions').get(inter.locale),
                value = permissions,
                inline = False
            )
        await inter.send(embeds=[embed], ephemeral = True)

def setup(bot: commands.Bot) -> NoReturn:
    bot.add_cog(HelpCommand(bot))
