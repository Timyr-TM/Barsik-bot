import disnake

from disnake.ext import commands
from typing import NoReturn, Union, Optional
from ..utils.bot_locale import BotLocal


class ClearCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name = "clear",
        description = BotLocal("slash_command.clear").get_localized,
        dm_permission = False,
        default_member_permissions = disnake.Permissions(
            manage_messages = True
        )
    )
    @commands.guild_only()
    @commands.bot_has_permissions(
        manage_messages = True
    )
    async def clear_command(
        self,
        inter: disnake.GuildCommandInteraction,
        count: int = commands.Param(
            name = "count",
            description = BotLocal("slash_command.clear.options.count").get_localized
        ),
        channel: Optional[Union[disnake.TextChannel, disnake.VoiceChannel]] = commands.Param(
            default = None,
            name = "channel",
            description = BotLocal("slash_command.clear.options.channel").get_localized
        ),
        member: Optional[disnake.Member] = commands.Param(
            default = None,
            name = "member",
            description = BotLocal("slash_command.clear.options.member").get_localized
        )
    ) -> NoReturn:
        await inter.response.defer(ephemeral = True)

        message = await inter.original_response()

        channel: Union[disnake.TextChannel, disnake.VoiceChannel] = channel or inter.channel

        embed_cleaning = disnake.Embed(
            title = f":wastebasket: {BotLocal('slash_command.clear.embed_cleaning').get(inter.locale)}",
            color = disnake.Color.dark_theme()
        )
        await inter.edit_original_response(
            embeds = [embed_cleaning]
        )

        del_messages = await channel.purge(
            limit = count,
            check = lambda mes: (member and member == mes.author) or True
        )

        description_member: str = (
            f"**{BotLocal('slash_command.clear.final_embed.description.member').get(inter.locale)}**: {member.mention}"
            if member
            else ""
        )
        final_embed = disnake.Embed(
            title = f":white_check_mark: {BotLocal('slash_command.clear.final_embed').get(inter.locale)}",
            color = disnake.Color.green()
        )
        await inter.edit_original_response(
            embeds = [final_embed]
        )
        system_embed = disnake.Embed(
            title = BotLocal("slash_command.clear.final_embed").get(inter.guild_locale),
            description = (
                f"**{BotLocal('slash_command.clear.final_embed.description.messages').get(inter.guild_locale)}**: "
                f"`{len(del_messages)}`\n"
                f"**{BotLocal('slash_command.clear.final_embed.description.channel').get(inter.guild_locale)}**: "
                f"{channel.mention}\n"
                f"**{BotLocal('slash_command.clear.final_embed.description.administrator').get(inter.guild_locale)}**: "
                f"{inter.author.mention}\n"
                f"{description_member}"
            ),
            color = disnake.Color.blurple()
        )
        await channel.send(
            embeds = [system_embed]
        )
def setup(bot: commands.Bot) -> NoReturn:
    bot.add_cog(ClearCommand(bot))
