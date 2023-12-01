from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from utils.states import SwitchWebsite

from keyboards import reply

from config import analyzed_website_file, time_interval_file, spell_check_accuracy_file

from data.subwriter import write_to_file

from filters.is_valid_url import is_valid_url


# When we use a router, the search for a suitable handler goes from top to bottom.
router = Router()


# Decorator that defines a handler for the "✅ switch website" message event
@router.message(F.text.lower().in_(["✅ switch website"]))
# Asynchronous function that handles fill new url based on a message object and state.
async def fill_new_url(message: Message, state: FSMContext):
    from handlers.user_commands import scheduled_task
    # Check if `scheduled_task` is defined and not yet completed
    if scheduled_task and not scheduled_task.done():
        # Cancel the `scheduled_task` if it is still running
        scheduled_task.cancel()

    # Set the state to 'waiting_for_url', using the `await` keyword for asynchronous execution
    await state.set_state(SwitchWebsite.waiting_for_url)
    # Send a message reply
    await message.answer(f"🌍 Enter <b>New Website URL</b>:")


@router.message(SwitchWebsite.waiting_for_url)
# Asynchronous function that handles form waiting for url based on a message object and state.
async def form_waiting_for_url(message: Message, state: FSMContext):
    new_website_url = message.text
    # Checks if entered test is a valid url
    if is_valid_url(new_website_url):
        # Update the data in the state with the value of `message.text` under the key 'waiting_for_url'
        await state.update_data(waiting_for_url=message.text)
        # Set the state to 'waiting_for_time_interval', using the `await` keyword for asynchronous execution
        await state.set_state(SwitchWebsite.waiting_for_time_interval)
        # Send a message replies
        await message.answer(f"✅ Great, <b>New Website URL</b> 🌍: <b>{message.text}</b>", reply_markup=reply.admin_main)
        await message.answer("⏰ Enter <b>New</b> Website Analysis <b>Time Interval</b> in seconds:")
        # Write New Website URL to the file
        write_to_file(analyzed_website_file, new_website_url)
    else:
        # Send a message reply
        await message.reply(
            f"❌ The specified text is <b>not a valid URL</b>. Please try again. Example: https://pоlito.uz"
        )


@router.message(SwitchWebsite.waiting_for_time_interval)
# Asynchronous function that handles form waiting for time interval based on a message object and state.
async def form_waiting_for_time_interval(message: Message, state: FSMContext):
    new_time_interval = message.text
    # Checks if entered value is int
    if new_time_interval.isdigit():
        # Update the data in the state with the value of `message.text` under the key 'waiting_for_time_interval'
        await state.update_data(waiting_for_time_interval=message.text)
        # Set the state to 'waiting_for_spell_check_accuracy', using the `await` keyword for asynchronous execution
        await state.set_state(SwitchWebsite.waiting_for_spell_check_accuracy)
        # Send a message replies
        await message.answer(f"✅ Great, <b>New Time Interval</b> ⏰: <b>{message.text}</b> seconds")
        await message.answer("📝 Enter <b>New Spell Check Accuracy</b> (0-1). Example: 0.9")
        # Write New Time Interval to the file
        write_to_file(time_interval_file, new_time_interval)
    else:
        # Send a message reply
        await message.reply("❌ The specified text is <b>not a valid time interval</b>. Please try again. Example: 3600")


@router.message(SwitchWebsite.waiting_for_spell_check_accuracy)
# Asynchronous function that handles form waiting for spell check accuracy based on a message object and state.
async def form_waiting_for_spell_check_accuracy(message: Message, state: FSMContext):
    new_spell_check_accuracy = message.text
    # Checks is entered value is float in range from 0 to 1
    try:
        new_spell_check_accuracy_float = float(new_spell_check_accuracy)
        # Checks if new_spell_check_accuracy_float is in range from 0 to 1
        if 0 <= new_spell_check_accuracy_float <= 1:
            # Update the data in the state with the value of `message.text`
            # under the key 'waiting_for_spell_check_accuracy'
            await state.update_data(waiting_for_spell_check_accuracy=message.text)
            # Send a message reply
            await message.answer(f"✅ Great, <b>New Spell Check Accuracy</b> 📝: <b>{message.text}</b>")
            new_spell_check_accuracy_str = str(new_spell_check_accuracy_float)
            # Write New Spell Check Accuracy to the file
            write_to_file(spell_check_accuracy_file, new_spell_check_accuracy_str)
            # data = await state.get_data()
            await state.clear()
            # Send a message reply and a certain keyboard
            await message.answer(
                f"🔄 <b>Restart</b> the Bot to Start the Analysis : <b>/start</b>",
                reply_markup=reply.admin_main
            )
        else:
            # Send a message reply
            await message.reply(
                "❌ The specified text is <b>not a valid spell check accuracy</b>. Please try again. Example: 0.9")

    except ValueError:
        # Send a message reply
        await message.reply(
            "❌ The specified text is <b>not a valid spell check accuracy</b>. Please try again. Example: 0.9")
