from aiogram import types, Bot
from filters import IsPrivate
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, InputMedia, CallbackQuery
from keyboards.default.default_btn import main_btn
from keyboards.inline.inline_btn import savatcha_btn, change_sells_pro, build_keyboard
from loader import dp, db, bot
from aiogram.dispatcher import FSMContext
import sqlite3
from data.products import prices
from states.reg_state import show_buy



@dp.message_handler(IsPrivate(), text="🛍 Savat")
async def savatcha_func(message: types.Message, state=FSMContext):
    # await message.delete()
    user_id = message.from_user.id
    # sells_pro = db.select_sells_product(user_id, user_id)
    name = db.select_user(user_id, user_id)[1]
    
    pro_sells = db.select_sells_product(user_id, user_id)
    
    pro_dict = {}
    
    pro_text =     ""
    raqam = 0
    narx = 0
    # yetkazish = 0
 
    if pro_sells:
        yetkazish = 8999

        for i in pro_sells:
            if i[2] in pro_dict:
                pro_dict[i[2]] = pro_dict[i[2]] + 1
            else:
                pro_dict[i[2]] = 1
            
        for id in pro_dict:
            raqam += 1
            
            product = db.select_product(id, id)
            print(pro_dict)
            print(product)
            
            pro_text += f"{raqam}. id: {product[0]} - {product[1]}: \n \t  {product[3]} x {pro_dict[id]} ta  =  {pro_dict[id] * product[3]} so'm \n"
            narx += pro_dict[id] * product[3]
            
        pro_text += f"\n\nYetkazib berish: {yetkazish} so'm \n"
            
        matn = f"{name} siz tanlagan mahsulotlar ro'yxati \n\n"
        matn += pro_text
        
        matn += f"\n Jami: {narx+yetkazish} so'm"
        
        await message.answer(matn, reply_markup=savatcha_btn())


    else:
        matn = "Siz hali buyurtmalar yo'q!\n"
        await message.reply(matn, reply_markup=main_btn)
    
   


@dp.callback_query_handler(text="change_sell_pro", state=None)
async def select_pro(call: CallbackQuery, state = FSMContext):
    await call.message.delete()
    user_id = call.from_user.id
    await call.message.answer("Maxsulotlaringizni saralang", reply_markup=ReplyKeyboardRemove())

    pro_count = db.select_sells_product(user_id, user_id)
        
            
    pro_text = ""
    pro_dict = {}
    narx = 0
    raqam = 0
    if pro_count:
        for i in pro_count:
            if i[2] in pro_dict:
                pro_dict[i[2]] = pro_dict[i[2]] + 1
            else:
                pro_dict[i[2]] = 1
        ############################################################################
            
        for id in pro_dict:
            raqam += 1
            
            product = db.select_product(id, id)
            # print(pro_dict)
            # print(product)
            
            pro_text += f"{raqam}. id: {product[0]} - {product[1]}: \n \t  {product[3]} x {pro_dict[id]} ta  =  {pro_dict[id] * product[3]} so'm \n"
            narx += pro_dict[id] * product[3]
        pro_text += f"\nJami: {narx}"
        

    await call.message.answer(pro_text, reply_markup=change_sells_pro(user_id))
    await state.set_state("del-product")


@dp.callback_query_handler(text="back_sell", state="del-product")
async def select_pro(call: CallbackQuery, state = FSMContext):
    await call.message.delete()
    await state.finish()
    user_id = call.from_user.id
    name = db.select_user(user_id, user_id)[1]
    
    pro_sells = db.select_sells_product(user_id, user_id)
    
    pro_dict = {}
    pro_text =     ""
    raqam = 0
    narx = 0
    yetkazish = 0
    if pro_sells:
        yetkazish = 8999

        for i in pro_sells:
            if i[2] in pro_dict:
                pro_dict[i[2]] = pro_dict[i[2]] + 1
            else:
                pro_dict[i[2]] = 1
            
        for id in pro_dict:
            raqam += 1
            
            product = db.select_product(id, id)
            
            pro_text += f"{raqam}. #id{product[0]}  {product[1]} - {pro_dict[id]} ta  =  {pro_dict[id] * product[3]} so'm \n"
            narx += pro_dict[id]*product[3]
            
        pro_text += f"\n\nYetkazib berish: {yetkazish} so'm \n"
        
    else:
        pro_text = "Siz hali buyurtmalar yo'q!\n"
    
    
    matn = f"{name} siz tanlagan mahsulotlar ro'yxati \n\n"
    matn += pro_text
    
    matn += f"\n Jami: {narx+yetkazish} so'm"
    
    await call.message.answer("Sizning xarid qilmoqchi bo'lgan mahsulotlaringiz", reply_markup=main_btn)
    await call.message.answer(matn, reply_markup=savatcha_btn())



@dp.callback_query_handler( state="del-product")
async def select_pro(call: CallbackQuery, state = FSMContext):
    user_id = call.from_user.id
    pro_count = db.select_sells_product(user_id, user_id)
   
    pro_text = ""
    pro_dict = {}
    narx = 0
    raqam = 0
    if pro_count:
        for i in pro_count:
            if i[2] in pro_dict:
                pro_dict[i[2]] = pro_dict[i[2]] + 1
            else:
                pro_dict[i[2]] = 1
        
    
        for id in pro_dict:
            raqam += 1
            
            product = db.select_product(id, id)
            # print(pro_dict)
            # print(product)
            
            pro_text += f"{raqam}. id: {product[0]} - {product[1]}: \n \t  {product[3]} x {pro_dict[id]} ta  =  {pro_dict[id] * product[3]} so'm \n"
            narx += pro_dict[id] * product[3]
    if call.data[:5] == "soni:":
        pro_id = call.data[5:]
     
        await call.answer(f"Bu mahsulotdan {pro_dict[int(pro_id)]} dona")
    elif call.data[:6] == "pulus:":
        pro_id = call.data[6:]
        print("pro id------",pro_id)
        db.add_sell_product(user_id, pro_id)
        
        pro_count = db.select_sells_product(user_id, user_id)
    
        pro_text = ""
        pro_dict = {}
        narx = 0
        raqam = 0
        if pro_count:
            for i in pro_count:
                if i[2] in pro_dict:
                    pro_dict[i[2]] = pro_dict[i[2]] + 1
                else:
                    pro_dict[i[2]] = 1
            
        
            for id in pro_dict:
                raqam += 1
                
                product = db.select_product(id, id)
                # print(pro_dict)
                # print(product)
                
                pro_text += f"{raqam}. id: {product[0]} - {product[1]}: \n \t  {product[3]} x {pro_dict[id]} ta  =  {pro_dict[id] * product[3]} so'm \n"
                narx += pro_dict[id] * product[3]
            pro_text += f"\nJami: {narx}"
            
        # await bot.edit_message_media(media=InputMedia(caption = pro_text), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=change_sells_pro(user_id))	
        await bot.edit_message_text(text=pro_text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=change_sells_pro(user_id)) 
        # await bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,caption=pro_text ,reply_markup=change_sells_pro(user_id))
    elif call.data[:6] == "minus:":
        pro_id = call.data[6:]
        print("pro id---minus---",pro_id)
        # db.add_sell_product(user_id, pro_id)
        
        pro_count = db.select_sells_product(user_id, user_id)
    
        pro_text = ""
        pro_dict = {}
        narx = 0
        raqam = 0
        if pro_count:
            for i in pro_count:
                if i[2] in pro_dict:
                    pro_dict[i[2]] = pro_dict[i[2]] + 1
                else:
                    pro_dict[i[2]] = 1
            ############################################################################
        db.delete_sells_product(user_id, int(pro_id))
        baza_soni=pro_dict[int(pro_id)]
        
        for son in range(1, baza_soni):
            db.add_sell_product(user_id, int(pro_id))

        pro_count = db.select_sells_product(user_id, user_id)
            
                
        pro_text = ""
        pro_dict = {}
        narx = 0
        raqam = 0
        if pro_count:
            for i in pro_count:
                if i[2] in pro_dict:
                    pro_dict[i[2]] = pro_dict[i[2]] + 1
                else:
                    pro_dict[i[2]] = 1
            ############################################################################
            # print("1-1-1-1--1-11-1-1-1----", pro_dict[int(pro_id)]==1)
            # if pro_id in pro_dict:
            if 1==1:
                for id in pro_dict:
                    raqam += 1
                    
                    product = db.select_product(id, id)
                    # print(pro_dict)
                    # print(product)
                    
                    pro_text += f"{raqam}. id: {product[0]} - {product[1]}: \n \t  {product[3]} x {pro_dict[id]} ta  =  {pro_dict[id] * product[3]} so'm \n"
                    narx += pro_dict[id] * product[3]
                pro_text += f"\nJami: {narx}"
                await bot.edit_message_text(text=pro_text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=change_sells_pro(user_id)) 
            else:   
                await bot.edit_message_text(text=pro_text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=change_sells_pro(user_id)) 
            await state.set_state("del-product")

        else:
            await call.message.delete()
            await state.finish()
            await call.message.answer("Sizda maxsulotlar qolmadi. Savatchangizni to'ldirib qaytadan urinib ko'ring.", reply_markup=main_btn)
            # await bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,caption="Sizda maxsulotlar qolmadi" ,reply_markup=change_sells_pro(user_id))
              
            ### await bot.edit_message_media(media=InputMedia(caption = pro_text), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=change_sells_pro(user_id))	
          
    # pro_id = call.data
    # # matn = "Qaysi mahsulotni olib tashlamoqchisiz? Savatdan olib tashlamoqchi bo'lgan mahsulotingiz ustiga bosing."
    # # db.delete_sells_product(user_id, pro_id)
    # prices.clear()
    # # await bot.edit_message_media(media=InputMedia(caption = matn), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=change_sells_pro(user_id))	
    # try:
        
    #     await bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,caption=matn ,reply_markup=change_sells_pro(user_id))

    # except :
    #     pass
    # await call.answer("Maxsulot o'chirildi")
    
    

@dp.callback_query_handler(text="delete_sells")
async def select_pro(call: CallbackQuery):
    await call.message.delete()
    user_id = call.from_user.id
    
    db.delete_sells_all_product(user_id, user_id)
   
    prices.clear()
    
    await call.message.answer("✅ Savatcha bo'shatildi")
    await call.message.answer("Bosh sahifa", reply_markup=main_btn)