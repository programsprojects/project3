from aiogram.filters.state import StatesGroup, State


# Switch Website class
class SwitchWebsite(StatesGroup):
    waiting_for_url = State()
    waiting_for_time_interval = State()
    waiting_for_spell_check_accuracy = State()
