import disnake
import os
from loguru import logger
from pathlib import Path
from disnake.ext import commands
from .utils.bot_config import BotConfig

config: dict = BotConfig.load()


bot = commands.Bot(
    intents=disnake.Intents.all(),
    command_prefix=commands.when_mentioned,
    help_command=None,
    description=(
        config["description"]
        if (description := config["description"]) and len(description) > 0
        else None
    ),
    reload=True,
    owner_ids=tuple(config["owners"]),
)

logger.add(config["log_file"])


def main():
    os.system("clear||cls")

    for path in Path(config.get("cogs")).glob("**/*.py"):
        parh_key = ".".join(path.parts)[:-3]
        logger.info(f"Load: {parh_key}")
        bot.load_extension(parh_key)
    bot.run(config["token"])


if __name__ == "__main__":
    main()
