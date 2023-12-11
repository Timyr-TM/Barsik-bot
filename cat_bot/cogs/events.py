import disnake
from loguru import logger
from disnake.ext import commands
from typing import NoReturn
from ..utils.bot_locale import BotLocal


class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener(disnake.Event.command_error)
    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> NoReturn:
        if isinstance(error, commands.CommandNotFound):
            return
        return

    @commands.Cog.listener(disnake.Event.connect)
    async def on_connect(self):
        logger.info(f"Bot connect: {self.bot.user.name} ({self.bot.user.id})")
        logger.info(f"Bot ping: {round(self.bot.latency / 1000, 3)}ms")

    @commands.Cog.listener(disnake.Event.disconnect)
    async def on_disconnect(self):
        logger.error(f"Bot disconnect")

    @commands.Cog.listener(disnake.Event.slash_command_completion)
    @commands.Cog.listener(disnake.Event.user_command_completion)
    @commands.Cog.listener(disnake.Event.message_command_completion)
    async def on_command_completion(self, inter: disnake.ApplicationCommandInteraction) -> NoReturn:
        logger.info(
            f"use: {inter.application_command.qualified_name}, user: {inter.author.name} ({inter.author.id})"
        )
        return

    @commands.Cog.listener(disnake.Event.slash_command_error)
    async def on_slash_command_error(
        self,
        inter: disnake.ApplicationCommandInteraction,
        error: commands.CommandError
    ) -> NoReturn:
        embed = disnake.Embed(
            title = BotLocal(f'error.slash_command').get(inter.locale),
            color = disnake.Color.brand_red()
        )
        if isinstance(error, commands.BotMissingPermissions):
            missing_permissions = []
            for permission in error.missing_permissions:
                missing_permissions.append(BotLocal(f'permission.{permission}').get(inter.locale))
            embed.description = f"{BotLocal('error.bot_missing_permissions').get(inter.locale)} {', '.join(...)}"
        else:
            embed.description = "..."
        await inter.send(
            embeds = [embed],
            ephemeral = True
        )
        return


def setup(bot: commands.Bot) -> NoReturn:
    bot.add_cog(Events(bot))
