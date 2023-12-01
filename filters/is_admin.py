from typing import List

from aiogram.filters import BaseFilter
from aiogram.types import Message


# Checks if user is admin
class IsAdmin(BaseFilter):

    # Initializes the class instance with the given user ids.
    # The user_ids can either be a single integer or a list of integers.
    def __init__(self, user_ids: int | List[int]) -> None:
        # Initialize the `user_ids` attribute with the provided `user_ids` value
        self.user_ids = user_ids

    # Defines the behavior of calling an instance of the class as a function.
    # Takes in a message object and returns a boolean value.
    async def __call__(self, message: Message) -> bool:
        # Check if `user_ids` is an integer
        if isinstance(self.user_ids, int):
            # Return a boolean indicating if the user id of the message matches `user_ids`
            return message.from_user.id == self.user_ids
        # Check if the user id of the message is in the list of user ids `user_ids`
        return message.from_user.id in self.user_ids
