import sys
import disnake
from loguru import logger
from barsik_bot import BarsikBot


def main(*args):
    bot = BarsikBot(intents=disnake.Intents.all())
    if len(args) == 0:
        if not bot.config.load():
            logger.error(
                'config not found! run "poetry por bot --gen-config" to generate the config'
            )
            exit(1)
        logger.remove(0)
        logger.add(sink=sys.stdout, format=bot.config.get("log-format"))
        logger.add(
            sink=bot.config.get("files.logs"), format=bot.config.get("log-format")
        )
        logger.info("start!")
        bot.i18n.load(bot.config.get("files.locals"))
        bot.docs.load(bot.config.get("files.docs"))
        bot.error_handler.load()
        bot.load_extensions()
        bot.run()
    elif args[0] == "--gen-config":
        logger.info("start gen config!")
        bot.config.generate()
        exit(0)


if __name__ == "__main__":
    main(*sys.argv[1:])
