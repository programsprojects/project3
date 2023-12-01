from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)

from config import switch_website, switch_website_yes, switch_website_no
from config import restart_bot, restart_bot_yes, restart_bot_no


# main admin keyboard
admin_main = ReplyKeyboardMarkup(
    # Creates Keyboard
    keyboard=[
        [
            # Creates Keyboard Buttons
            KeyboardButton(text=switch_website),
            KeyboardButton(text=restart_bot)
        ]
    ],
    # Allows the keyboard to be resized in the chat window
    resize_keyboard=True,
    # Makes the keyboard disappear after a button is pressed
    one_time_keyboard=True,
    # Specifies the placeholder text displayed in the input field
    input_field_placeholder="Select an action from the menu",
    # Keyboard should only be shown to specific users
    selective=True
)


# admin switch website keyboard
admin_switch_website = ReplyKeyboardMarkup(
    # Creates Keyboard
    keyboard=[
        [
            # Creates Keyboard Buttons
            KeyboardButton(text=switch_website_yes),
            KeyboardButton(text=switch_website_no)
        ]
    ],
    # Allows the keyboard to be resized in the chat window
    resize_keyboard=True,
    # Makes the keyboard disappear after a button is pressed
    one_time_keyboard=True,
    # Specifies the placeholder text displayed in the input field
    input_field_placeholder="Select an action from the menu",
    # Keyboard should only be shown to specific users
    selective=True
)


# main user keyboard
user_main = ReplyKeyboardMarkup(
    # Creates Keyboard
    keyboard=[
        [
            # Creates a Keyboard Button
            KeyboardButton(text=restart_bot)
        ]
    ],
    # Allows the keyboard to be resized in the chat window
    resize_keyboard=True,
    # Makes the keyboard disappear after a button is pressed
    one_time_keyboard=True,
    # Specifies the placeholder text displayed in the input field
    input_field_placeholder="Select an action from the menu",
    # Keyboard should only be shown to specific users
    selective=True
)


# restart keyboard
restart = ReplyKeyboardMarkup(
    # Creates Keyboard
    keyboard=[
        [
            # Creates Keyboard Buttons
            KeyboardButton(text=restart_bot_yes),
            KeyboardButton(text=restart_bot_no)
        ]
    ],
    # Allows the keyboard to be resized in the chat window
    resize_keyboard=True,
    # Makes the keyboard disappear after a button is pressed
    one_time_keyboard=True,
    # Specifies the placeholder text displayed in the input field
    input_field_placeholder="Select an action from the menu",
    # Keyboard should only be shown to specific users
    selective=True
)

# keyboard remove
rmk = ReplyKeyboardRemove()
