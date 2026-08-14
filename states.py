from aiogram.fsm.state import State, StatesGroup


class AnonMessageStates(StatesGroup):
    waiting_for_message = State()   # Boshqa userga anonim xabar yozayotganda
    waiting_for_reply = State()     # Kelgan xabarga javob yozayotganda


class AdStates(StatesGroup):
    waiting_for_ad_message = State()   # Reklama bo'limiga xabar yozayotganda


class PollStates(StatesGroup):
    waiting_for_question = State()   # So'rovnoma savolini kutish
    waiting_for_options = State()    # So'rovnoma variantlarini kutish
