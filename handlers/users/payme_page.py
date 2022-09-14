from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, Message
from data.config import ADMINS, CHANEL_CHAT_ID
from datetime import datetime

from loader import dp, bot, db
from data.products import products_,  FAST_SHIPPING, REGULAR_SHIPPING, PICKUP_SHIPPING, funci, prices
from keyboards.inline.inline_btn import build_keyboard
from keyboards.default.default_btn import main_btn
import sqlite3



@dp.callback_query_handler(text="payme_card")
async def book_invoice(call: CallbackQuery):

    print("ishladi 1")
    user_id = call.from_user.id
    
    global kuser_id
    kuser_id = user_id  
    prices.clear()
    await funci(user_id)
    
    pro_sells = db.select_sells_product(user_id, user_id)
    pro_dict = {}
    pro_text = "\n"
    narx = 0
    for i in pro_sells:
        if i[2] in pro_dict:
            pro_dict[i[2]] = pro_dict[i[2]] + 1
        else:
            pro_dict[i[2]] = 1
        
    
    for id in pro_dict:
        
        
        product = db.select_product(id, id)
        
        pro_text += f"{product[1]} - {pro_dict[id]} ta  \n"
        narx += pro_dict[id]*product[3]
        
    # pro_payment(narx, pro_text)
    print("ishladi 2")
    pro_text += f"Jami xarajat: {narx} so'm\n"
    
    # date = datetime.now()
    
    # db.add_sells_products(user_id, pro_text, narx, date, 0)
    try:
        
        await bot.send_invoice(chat_id=call.from_user.id,
                            **products_.generate_invoice(),
                            payload=pro_text,
                            )
        await call.answer()
        await call.message.delete()

    except :
        await call.message.answer("Maxsulot turini kamaytiring. Biz bir vaqtda faqat 5 turdagi maxsulotlarni qabul qila olamiz. ")
    
    print("ishladi 3")
    # await call.message.delete()



@dp.shipping_query_handler()
async def choose_shipping(query: types.ShippingQuery):
    if query.shipping_address.country_code != "UZ":
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        ok=False,
                                        error_message="Chet elga yetkazib bera olmaymiz")
    elif query.shipping_address.city.lower() == "tashkent":
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        shipping_options=[FAST_SHIPPING, REGULAR_SHIPPING, PICKUP_SHIPPING],
                                        ok=True)
    else:
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        shipping_options=[REGULAR_SHIPPING],
                                        ok=True)


@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    
    user_id = pre_checkout_query.from_user.id
    
    db.delete_sells_all_product(user_id, user_id)
    
    await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id,
                                        ok=True)
    await bot.send_message(chat_id=pre_checkout_query.from_user.id,
                           text="To'lovingiz qabul qilindi.  \n  Xaridingiz uchun rahmat! \n ")
        
    adress_data = pre_checkout_query.order_info.shipping_address
    client_adress = f"""
        State: {adress_data['state']},
        City: {adress_data['city']},
        Address 1: {adress_data['street_line1']},
        Address 2: {adress_data['street_line2']},
        Post code: {adress_data['post_code']}
    """
    
    check_sell1 =  f"#CHECK: {pre_checkout_query.id}\n\n"
    check_sell = f"Quyidagi mahsulot sotildi: {pre_checkout_query.invoice_payload}\n"
    check_sell += f"Telegram user: <a href='tg://user?id={pre_checkout_query.from_user.id}'> {pre_checkout_query.from_user.first_name}</a>\n"
    check_sell +=  f"Xaridor: {pre_checkout_query.order_info.name}\n"
    check_sell +=  f"Manzil: {client_adress}\n"
    check_sell +=  f"Tel: {pre_checkout_query.order_info.phone_number}"
    
    await bot.send_message(chat_id=pre_checkout_query.from_user.id,
                           text=check_sell1+check_sell,                                                              
                            )
    await bot.send_message(chat_id=pre_checkout_query.from_user.id,
                           text="Tez orada siz bilan bog'lanamiz. \nQandaydir muammo yuzaga kelsa biz bilan bog'laning:\nTelegram: @Jaloliddin_Mamatmusayev \nTelefon: +998932977419", reply_markup=main_btn)
    date = datetime.now()
    db.add_sells_products(user_id, check_sell, check_sell1, date)
    
    await bot.send_message(chat_id=CHANEL_CHAT_ID,
                           text=check_sell1+check_sell,
                           
                                                                                           
                            )
    
