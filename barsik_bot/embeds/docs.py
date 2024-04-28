from disnake import Colour, Embed, Locale

from barsik_bot import BarsikBot, Docs, SlashCommandDocs
from barsik_bot.utils import list_format


class DocsEmbed(Embed):
    def __init__(self, **options) -> None:
        self.docs: Docs = options.pop("docs")
        self.locale: Locale = options.pop("locale")
        self.bot: BarsikBot = options.pop("bot")
        super().__init__(
            title=str(self.docs),
            description=f"`{self.docs.id}`",
            color=Colour.blurple(),
        )


class SlashCommandDocsEmbed(Embed):
    def __init__(self, **options) -> None:
        self.docs: SlashCommandDocs = options.pop("docs")
        self.locale: Locale = options.pop("locale")
        self.bot: BarsikBot = options.pop("bot")
        super().__init__(
            title=self.bot.i18n.get(
                "embed.docs.slash-command.title",
                self.locale,
                command=(
                    str(self.docs)
                    if not (slash := self.bot.get_global_command_named(self.docs.name))
                    else "</%s:%s>" % (self.docs.name, str(slash.id))
                ),
            ),
            description=self.bot.i18n.get(self.docs.description, self.locale),
            color=Colour.blurple(),
        )
        self.set_thumbnail(
            "https://cdn.discordapp.com/emojis/1231533578496508004.webp?size=160"
        )
        if self.docs.options is not None:
            self.add_field(
                name=self.bot.i18n.get("embed.docs.slash-command.options", self.locale),
                value=list_format(
                    [
                        "**{name}** {required}\n {description}".format(
                            name=option.name,
                            description=self.bot.i18n.get(
                                option.description, self.locale
                            ),
                            required="🔹" if option.required else "",
                        )
                        for option in sorted(
                            self.docs.options, key=lambda item: item.required
                        )
                    ]
                ),
                inline=False,
            )
        if self.docs.permissions:
            self.add_field(
                name=self.bot.i18n.get(
                    "embed.docs.slash-command.permissions", self.locale
                ),
                value=", ".join(
                    [
                        f"`{(self.bot.i18n.get(f'permission.{permission}', self.locale))}`"
                        for permission in self.docs.permissions
                    ]
                ),
            )

    def formated_option(self, name: str, description: str, required: bool) -> str:
        data = (
            "**{name}** `({required})`\n {description}"
            if required
            else "**{name}**\n {description}"
        )
        return data.format(
            name=name,
            description=self.bot.i18n.get(description, self.locale),
            required=self.bot.i18n.get(
                "embed.docs.slash-command.option-required", self.locale
            ),
        )


def docs_to_embed(docs: Docs, locale: Locale, bot: BarsikBot) -> Embed:
    embeds = {Docs: DocsEmbed, SlashCommandDocs: SlashCommandDocsEmbed}
    return embeds.get(type(docs), DocsEmbed)(docs=docs, locale=locale, bot=bot)
