from aiogram.dispatcher.filters.state import State, StatesGroup

class FSMSearch(StatesGroup):
    field = State()
    contacts = State()



