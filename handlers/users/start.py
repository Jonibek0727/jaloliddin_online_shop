from aiogram import types , Bot
from aiogram.dispatcher.filters.builtin import CommandStart
from filters import IsPrivate
from datetime import datetime
from keyboards.inline.inline_btn import select_lang
from keyboards.default.default_btn import phone_num, regions_btn, main_btn, admin_main_btn
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, CallbackQuery
from aiogram import md
from aiogram.utils import markdown
from aiogram.dispatcher import FSMContext
from states.reg_state import reg_user

from loader import dp, db, bot
import sqlite3
import re

from data.config import CHANEL_CHAT_ID
from data.config import ADMINS



PHONE_NUM = r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$'
PHONE_NUM_2 = r'^[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$'



@dp.message_handler(CommandStart(), IsPrivate(),  user_id=ADMINS)
async def bot_start(message: types.Message):
    await message.answer("Assalomu alaykum admin. Botga xush kelibsiz.", reply_markup=admin_main_btn)


@dp.message_handler(CommandStart(), IsPrivate(), state=None)
async def bot_start(message: types.Message):
    tg_id = message.from_user.id
    if not db.select_user(tg_id, tg_id):
        name = message.from_user.full_name
        tg_id = message.from_user.id
        today = datetime.now().date()
        try:
            db.add_user(id=tg_id,
                        
                        name=name, 
                        date_of_start=today,
                        )
            # await bot.send_message(GROUP_CHAT_ID, f"{name} start bosdi.\nid:<a href='tg://user?id={message.from_user.id}'> {message.from_user.id} </a>")
        except sqlite3.IntegrityError as err:
            pass
        
        
        await message.answer(f"Salom, {md.quote_html(message.from_user.full_name)}! ")
        await message.answer(f" O'zingizga qulay tilni tanlang 🇺🇿 / 🇷🇺  \n    ------------------------------------------  \n Выберите предпочитаемый язык 🇷🇺 / 🇺🇿 ", reply_markup=select_lang)
        await reg_user.lang.set()
    else:
        await message.answer(f"Assalomu alaykum {md.quote_html(message.from_user.full_name)}. Botga xush kelibsiz", reply_markup=main_btn)
     
@dp.callback_query_handler(text="uzbek", state=reg_user.lang)
async def select_lang_func(call: CallbackQuery, state:FSMContext):
	lang = 'uzbek'
	await state.update_data(
        {"lang":lang}
    )
	await call.message.delete()
	await call.message.answer("Ism Familiyangizni kiriting (faqat harflarda kiriitng). \n \n <i><b>Masalan: </b> Jaloliddin Mamatmusayev </i>")
	await reg_user.name.set()
    
    
    

@dp.message_handler( state=reg_user.name)
async def user_name(message: types.Message, state:FSMContext):
   
    name = message.text
    c=0
    for i in name:
        if i.isnumeric():
            c+=1
        
        
    if not c:
        await state.update_data(
			{"name":name}
		)
        print("ismda faqat harflar")
        await message.answer("Telefon raqamingizni to'liq formatda kiriting: \n \n <i><b>Masalan: </b> +998912345678 </i>", reply_markup=phone_num)
        await reg_user.phone.set()
    else:
        await message.answer("Ismingizda faqat harflar bo'lishi kerak!")
        await reg_user.name.set()

  

@dp.message_handler( state=reg_user.phone, content_types=["contact","text"])
async def user_name(message: types.Message, state:FSMContext):
    phone = message
    
    if phone.text:
        if phone.text[:4] == '+998' and  len(phone.text)==13:
            await state.update_data(
            	{"phone": phone.text}
            )
            await message.answer("Manzilni tanlang.", reply_markup=regions_btn)
            await reg_user.adress.set()
        else:
            await message.answer("❌ Noto'g'ri formatda terdingiz!, \nQaytadan kiriting!")
            
            await message.answer("Yoki quidagi tugma orqali jo'nating! 👇🏻", reply_markup=phone_num)
            await reg_user.phone.set()
    
    elif phone.contact:
        await state.update_data(
        	{"phone": phone.contact.phone_number}
        )
        await message.answer("Manzilni tanlang.", reply_markup=regions_btn)
        await reg_user.adress.set()
    else:
        await message.answer("❌ Noto'g'ri raqam terdingiz!, \nQaytadan kiriting!")
            
        await message.answer("Yoki quidagi tugma orqali jo'nating! 👇🏻", reply_markup=phone_num)
        await reg_user.phone.set()

    
    
    
    # await state.update_data(
    #     {"phone":phone}
    # )
    # await message.answer("Manzilni tanlang.")
    # await reg_user.adress.set()
	

@dp.message_handler( state=reg_user.adress)
async def user_name(message: types.Message, state:FSMContext):
    adress = message.text
    await state.update_data(
        {"adress":adress}
    )
    id = message.from_user.id
    
    data = await state.get_data()
    name = data.get("name")
    lang = data.get("lang")
    phone = data.get("phone")
    adress = data.get("adress")
    today = datetime.now().date()
    # print(today)
    db.add_reg_user(id, name, phone, adress, lang, 1, today)
    
    
    # await bot.send_message(CHANEL_CHAT_ID, f"{name} -- ro'yxatdan muvaffaqiyatli o'tdi \nTelegram: <a href='https://t.me/user?id={message.from_user.id}'>{message.from_user.full_name} </a> \nUser id: {message.from_user.id}")
    await state.finish()

    await message.answer("Ro'yxatdan muvaffaqiyatli o'tdingiz. Endi xaridingizni amalga oshirishingiz mumkin.", reply_markup=main_btn)
