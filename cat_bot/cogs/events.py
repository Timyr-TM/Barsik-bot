import disnake
from disnake.ext import commands
from typing import NoReturn


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


def setup(bot: commands.Bot) -> NoReturn:
    bot.add_cog(Events(bot))
