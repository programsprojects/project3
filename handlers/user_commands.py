from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

from keyboards import reply

from filters.is_admin import IsAdmin

from config import analyzed_website_file
from config import time_interval_file, spell_check_accuracy_file, is_content_changed_threshold

from config_reader import config

from data.subloader import read_from_file
from data.initial_data import InitialData

from utils.data_processing import get_initial_data, get_new_content, is_content_changed, find_urls_difference
from utils.data_processing import spell_check_new_post

import asyncio


# When we use a router, the search for a suitable handler goes from top to bottom.
router = Router()

# Create an instance of a class to store initial data.
initial_data = InitialData()

scheduled_task = None


# Code executed after CommandStart or "restart bot" handler is triggered
async def start(message, keyboard):
    # Declare the `scheduled_task` variable as a global variable
    global scheduled_task
    # Check if `scheduled_task` is defined and not yet completed
    if scheduled_task and not scheduled_task.done():
        # Cancel the `scheduled_task` if it is still running
        scheduled_task.cancel()

    # get user and chat id
    user_id = message.from_user.id
    chat_id = message.chat.id
    print("My id")
    print(user_id)
    print(chat_id)

    # Get data from the data files
    analyzed_website_url = read_from_file(analyzed_website_file)
    time_interval = int(read_from_file(time_interval_file))
    spell_check_accuracy_float = float(read_from_file(spell_check_accuracy_file))

    # Send a message replies
    await message.answer("🌍 Website is being Analyzed:")
    # Send a message reply with the url of analyzed website and a certain keyboard
    await message.answer(f"{analyzed_website_url}", reply_markup=keyboard)
    # Send a message reply with the time interval of analyzed website
    await message.answer(f"⏰ Website analyses every <b>{time_interval} seconds</b>")
    # Send a message reply with the spell check accuracy of analyzed website
    await message.answer(f"📝 Spell check accuracy is <b>{spell_check_accuracy_float}</b>")
    await message.answer("No new posts at the moment.")
    await message.answer("Please wait for new post ...")

    # Gets urls of new posts and all current urls on the website
    initial_content, initial_urls = await get_initial_data(analyzed_website_url)

    global initial_data
    # Updating data in the class instance.
    initial_data.initial_content = initial_content
    initial_data.initial_urls = initial_urls

    # Create a task using asyncio to schedule the `scheduled_job` function with the given parameters
    scheduled_task = asyncio.create_task(
        scheduled_job(message, time_interval, analyzed_website_url, spell_check_accuracy_float)
    )


# Scheduled job in a certain time interval, checks website for new posts and spell check each of them
async def scheduled_job(message, time_interval, analyzed_website_url, spell_check_accuracy_float):
    while True:
        # sleep for time_interval seconds
        await asyncio.sleep(time_interval)
        # await message.answer(f"Time interval in {time_interval} seconds is over.")

        global initial_data
        # Updating data in the class instance.
        initial_content = initial_data.initial_content
        initial_urls = initial_data.initial_urls

        # Get new content from the website
        new_content = await get_new_content(analyzed_website_url)

        # Checks if content was changed on the website
        if await is_content_changed(initial_content, new_content, is_content_changed_threshold):

            # Gets urls of new posts and all current urls on the website
            urls_difference, new_urls = await find_urls_difference(analyzed_website_url, initial_urls, new_content)

            if urls_difference is not None:
                # For each new post send a message reply with a certain content
                for url_difference in urls_difference:
                    # Send a message replies
                    await message.answer("📄 There is a new post.")
                    # Send a message reply with the url of a new post
                    await message.answer(f"{url_difference}")
                    await message.answer("📝 Spell check has begun.")
                    await message.answer("🙏 Please be patient as it may take some time.")

                    # Send a message reply with a new post spell check result
                    await spell_check_new_post(url_difference, message, spell_check_accuracy_float)
                    await message.answer("📝 Spell check is over.")

                    # Updating data in the class instance.
                    initial_data.initial_content = new_content
                    initial_data.initial_urls = new_urls
            else:
                # await message.answer("Urls didn't change")
                print("Urls didn't change")

        else:
            # await message.answer("Content didn't change")
            print("Content didn't change")


# Decorator that defines a handler for the CommandStart event and checks if the user is an admin
@router.message(CommandStart(), IsAdmin(config.is_admin))
# Decorator that defines a handler for the "✅ restart bot" message event and checks if the user is an admin
@router.message(F.text.lower().in_("✅ restart bot"), IsAdmin(config.is_admin))
# Asynchronous function that handles start for admin based on a message object.
async def start_for_admin(message: Message) -> None:
    # set admin keyboard
    keyboard = reply.admin_main
    # Call the `start` function with the `message` and `keyboard` as parameters,
    # using the `await` keyword for asynchronous execution
    await start(message, keyboard)


# Decorator that defines a handler for the CommandStart event
@router.message(CommandStart())
# Decorator that defines a handler for the "restart bot" message event
@router.message(F.text.lower().in_("✅ restart bot"))
# Asynchronous function that handles start for user based on a message object.
async def start_for_user(message: Message):
    # set user keyboard
    keyboard = reply.user_main
    # Call the `start` function with the `message` and `keyboard` as parameters,
    # using the `await` keyword for asynchronous execution
    await start(message, keyboard)
