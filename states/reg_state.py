from aiogram.dispatcher.filters.state import StatesGroup,State



class reg_user(StatesGroup):

    lang = State()
    name = State()
    phone = State()
    adress = State()



class update_user(StatesGroup):

    lang = State()
    name = State()
    phone = State()
    adress = State()



class products(StatesGroup):

    name = State()
    caption = State()
    category = State()
    subcategory = State()
    price = State()
    photo = State()
    finish = State()
    


class show_buy(StatesGroup):
 
    category = State()
    subcategory = State()
    price = State()
    next = State()
    prev = State()



class savatcha_state(StatesGroup):
 
    category = State()
    subcategory = State()
    price = State()
    next = State()
    prev = State()
