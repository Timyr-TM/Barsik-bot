import datetime
import os
import disnake
import tomllib

from pathlib import Path
from disnake.ext import commands
from loguru import logger


def main():
    os.system("@cls||clear")
    data_time = datetime.datetime.now().strftime("%d.%m.%Y %H-%M-%S")
    logger.add(sink = f"./src/logs/{data_time}.log")
    config_file = Path("./config.toml")
    if config_file.exists():
        with config_file.open(mode = "rb") as file:
            config: dict = tomllib.load(file).get("bot").get("config")
    else:
        logger.error("Config: config.toml not found!")
        exit(1)

    bot = commands.Bot(
        intents = disnake.Intents.all(),
        command_prefix = commands.when_mentioned,
        help_command = None,
        reload = True,
        owner_ids = config.get("owners")
    )

    for path in Path("./cat_bot/cogs/").glob("**/*.py"):
        parh_key = ".".join(path.parts)[:-3]
        bot.load_extension(parh_key)
        logger.info(f"Load cog: {parh_key}")
    if not config.get("token"):
        logger.error(f"parameter \"token\" not found in pyproject.toml")
        exit(1)
    elif config.get("token") == "...":
        logger.error(f"parameter \"token\" is not specified in pyproject.toml")
        exit(1)
    else:
        bot.run(config.get("token"))


if __name__ == "__main__":
    main()
