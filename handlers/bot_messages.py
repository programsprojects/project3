import asyncio

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from keyboards import reply

from filters.is_admin import IsAdmin
from config_reader import config


# When we use a router, the search for a suitable handler goes from top to bottom.
router = Router()


# Decorator that defines a handler for the "hi" message event
@router.message(F.text.lower().in_("hi"))
# Asynchronous function that handles greetings based on a message object.
async def greetings(message: Message):
    # Send a message reply
    await message.reply("Hi!")
    # sleep for 1 second
    await asyncio.sleep(1)


# Decorator that defines a handler for the "hello" message event
@router.message(F.text.lower().in_("hello"))
# Asynchronous function that handles greetings based on a message object.
async def greetings(message: Message):
    # Send a message reply
    await message.reply("Hello!")
    # sleep for 1 second
    await asyncio.sleep(1)


# Decorator that defines a handler for the "🌍 switch website" message event and checks if the user is an admin
@router.message(F.text.lower().in_("🌍 switch website"), IsAdmin(config.is_admin))
# Asynchronous function that handles switch website based on a message object.
async def switch_website(message: Message):
    # Send a message reply
    await message.answer("Are you sure you want to Switch Website?", reply_markup=reply.admin_switch_website)
    # sleep for 1 second
    await asyncio.sleep(1)


# Decorator that defines a handler for the "❌ don't switch website" message event and checks if the user is an admin
@router.message(F.text.lower().in_("❌ don't switch website"), IsAdmin(config.is_admin))
# Asynchronous function that handles not switch website based on a message object.
async def not_switch_website(message: Message):
    # Send a message reply
    await message.answer("Switching website is canceled.", reply_markup=reply.admin_main)
    # sleep for 1 second
    await asyncio.sleep(1)


# Decorator that defines a handler for the "🔄 restart bot" message event
@router.message(F.text.lower().in_("🔄 restart bot"))
# Asynchronous function that handles restart bot based on a message object.
async def restart_bot(message: Message):
    # Send a message reply
    await message.answer("Are you sure you want to Restart bot?", reply_markup=reply.restart)
    # sleep for 1 second
    await asyncio.sleep(1)


# Decorator that defines a handler for the "❌ don't restart bot" message event and checks if the user is an admin
@router.message(F.text.lower().in_("❌ don't restart bot"), IsAdmin(config.is_admin))
# Asynchronous function that handles not restart bot admin based on a message object.
async def not_restart_bot_admin(message: Message):
    # Send a message reply
    await message.answer("Restarting bot is canceled.", reply_markup=reply.admin_main)
    # sleep for 1 second
    await asyncio.sleep(1)


# Decorator that defines a handler for the "❌ don't restart bot" message event
@router.message(F.text.lower().in_("❌ don't restart bot"))
# Asynchronous function that handles not restart bot user based on a message object.
async def not_restart_bot_user(message: Message):
    # Send a message reply
    await message.answer("Restarting bot is canceled.", reply_markup=reply.user_main)
    # sleep for 1 second
    await asyncio.sleep(1)


# Decorator that defines a handler for the "help" message and command /help event
@router.message(F.text.lower().in_("help"))
# Asynchronous function that handles help message based on a message object.
@router.message(Command("help"))
async def help_message(message: Message):
    # Send a message reply
    await message.answer("This bot can analyze a particular website 🌍 for changes and spell check 📝new posts. /start")
    # sleep for 1 second
    await asyncio.sleep(1)


# Decorator that defines a handler for message event when none of the handlers triggered
@router.message()
# Asynchronous function that handles echo based on a message object.
async def echo(message: Message):
    # Send a message reply
    await message.answer(f"Sorry, I don't understand you. 🤷‍♂️ Please try again. 🙏")
    # sleep for 1 second
    await asyncio.sleep(1)
