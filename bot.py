import asyncio

from aiogram import Bot, Dispatcher
from handlers import bot_messages, user_commands, new_website_url
from middlewares.antiflood import AntiFloodMiddleware
from config_reader import config

# logging information
import logging


async def main() -> None:
    # Set the logging level to INFO
    logging.basicConfig(level=logging.INFO)

    # Creating an instance of the Bot class with the bot token and parse_mode="HTML" let make text bold, italic
    bot = Bot(config.bot_token.get_secret_value(), parse_mode="HTML")
    # Creating an instance of the Dispatcher class
    dp = Dispatcher()

    # no earlier than number of seconds bot will react to the next command
    dp.message.middleware(AntiFloodMiddleware(1))

    # When we use a router, the search for a suitable handler goes from top to bottom.
    dp.include_routers(
        user_commands.router,
        new_website_url.router,
        bot_messages.router
    )

    # start without any backlog of updates.
    await bot.delete_webhook(drop_pending_updates=True)

    try:
        # Starts polling for updates using the `dp` object (presumably a Dispatcher)
        await dp.start_polling(bot)
    finally:
        # With the given `bot`. It ensures that the bot session is closed properly, even in case of an exception.
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
