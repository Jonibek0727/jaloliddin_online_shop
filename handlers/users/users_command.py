from aiogram import types , Bot
from keyboards.default.default_btn import main_btn, maktab_ichi, user_settings, phone_num, regions_btn, back_btn, bogcha_ichi
from keyboards.inline.inline_btn import select_lang, add_pocket, savatcha_btn, show_like_products
from filters import IsPrivate
from states.reg_state import update_user
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, CallbackQuery, InputMedia

from loader import dp, db, bot
from aiogram.dispatcher import FSMContext
import sqlite3



@dp.message_handler(IsPrivate(), text="🔙 Ortga")
async def bot_start(message: types.Message):
    await message.reply("Asosiy sahifa", reply_markup=main_btn)
    


@dp.message_handler(IsPrivate(), text="Bog'cha",  state=None)
async def bot_start(message: types.Message, state=FSMContext):
    await message.reply("Guruhni tanlang.", reply_markup=bogcha_ichi)
    

@dp.message_handler(IsPrivate(), text="Maktab",  state=None)
async def bot_start(message: types.Message, state=FSMContext):
    await message.reply("Guruhni tanlang.", reply_markup=maktab_ichi)
    
    
    
    
@dp.message_handler(IsPrivate(), text="⚙️ Sozlamalar",  state=None)
async def bot_start(message: types.Message, state=FSMContext):
    await message.reply("Qaysi bo'lim ma'lumotlarini tahrirlamoqchisiz?", reply_markup=user_settings)
    
    
    
@dp.message_handler(IsPrivate(), text="Tilni  🇺🇿 / 🇷🇺",  state=None)
async def bot_start(message: types.Message, state=FSMContext):
    await message.answer(f" O'zingizga qulay tilni tanlang 🇺🇿 / 🇷🇺  \n    ------------------------------------------  \n Выберите предпочитаемый язык 🇷🇺 / 🇺🇿 ", reply_markup=select_lang)
    await state.set_state("change_lang")

@dp.callback_query_handler( state="change_lang")
async def select_lang_func(call: CallbackQuery, state:FSMContext):
    print(call.data)
    try:
        if call.data=="uzbek":
            lang = 'uzbek'
            db.update_user_lan(lang, call.from_user.id)
        else:
            lang = 'russian'
            db.update_user_lan(lang, call.from_user.id)

    except Exception as err:
        print("tilni o'zgartirishda xatolik", err)
    await call.message.delete()
    await call.message.answer("⚙️ Sozlamalar", reply_markup=user_settings)
    await state.finish()
    
    
    
@dp.message_handler(IsPrivate(), text="👤 Shaxsiy ma'lumotlarni",  state=None)
async def bot_start(message: types.Message, state=FSMContext):
    await message.answer("Ism Familiyangizni kiriting (faqat harflarda kiriitng). \n \n <i><b>Masalan: </b> Jaloliddin Mamatmusayev </i>", reply_markup=ReplyKeyboardRemove())
    await update_user.name.set()

        
@dp.message_handler(IsPrivate(), state=update_user.name)
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
        # print("ismda faqat harflar")
        await message.answer("Telefon raqamingizni to'liq formatda kiriting: \n \n <i><b>Masalan: </b> +998912345678 </i>", reply_markup=phone_num)
        await update_user.phone.set()
    else:
        await message.answer("Ismingizda faqat harflar bo'lishi kerak!")
        await update_user.name.set()



@dp.message_handler(IsPrivate(),  state=update_user.phone, content_types=["contact","text"])
async def user_name(message: types.Message, state:FSMContext):
    phone = message
    
    if phone.text:
        if phone.text[:4] == '+998' and  len(phone.text)==13:
            await state.update_data(
            	{"phone": phone.text}
            )
            await message.answer("Manzilni tanlang.", reply_markup=regions_btn)
            await update_user.adress.set()
        else:
            await message.answer("❌ Noto'g'ri formatda terdingiz!, \nQaytadan kiriting!")
            
            await message.answer("Yoki quidagi tugma orqali jo'nating! 👇🏻", reply_markup=phone_num)
            await update_user.phone.set()
    
    elif phone.contact:
        await state.update_data(
        	{"phone": phone.contact.phone_number}
        )
        await message.answer("Manzilni tanlang.", reply_markup=regions_btn)
        await update_user.adress.set()
    else:
        await message.answer("❌ Noto'g'ri raqam terdingiz!, \nQaytadan kiriting!")
            
        await message.answer("Yoki quidagi tugma orqali jo'nating! 👇🏻", reply_markup=phone_num)
        await update_user.phone.set()



@dp.message_handler(IsPrivate(), state=update_user.adress)
async def user_name(message: types.Message, state:FSMContext):
    adress = message.text
    await state.update_data(
        {"adress":adress}
    )
    id = message.from_user.id
    
    data = await state.get_data()
    name = data.get("name")
   
    phone = data.get("phone")
    adress = data.get("adress")
    try:
        db.update_user_info(name, phone, adress, id)
    except Exception as err:
        print("yangilashda xatolik>>>>>", err)
        
        
    await message.answer("⚙️ Sozlamalar", reply_markup=user_settings)
    await state.finish()
    
        
        

## maxsulotni izlash ###
@dp.message_handler(text="🔎 Mahsulotni izlash", state=None)
async def send_ad_to_all(message: types.Message, state=FSMContext):
    await message.answer("Izlayotgan maxsulotingiz id sini yuboring:", reply_markup=back_btn)
    await state.set_state("find-pro3")

    
# @dp.callback_query_handler( state="find-pro")
# async def select_pro(call: CallbackQuery, state:FSMContext):
#     await call.message.delete()
#     db.delete_product(call.data, call.data)
#     await call.message.answer(f"#id : {call.data}  -  maxsulot o'chirildi ✅")
#     await call.message.answer("Bosh sahifa", reply_markup=admin_main_btn)
#     await state.finish()


@dp.message_handler(text="🔙 Ortga",state="find-pro3")
async def send_ad_to_all(message: types.Message, state=FSMContext):
    await message.answer("Bosh sahifa", reply_markup=main_btn)
    await state.finish()
    


@dp.callback_query_handler(text="payme",state="find-pro3")
async def select_pro(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.finish()
    await call.message.answer("Sizning savatchangizdagi mahsulotlar", reply_markup=main_btn)
    user_id = call.from_user.id
    
    name = db.select_user(user_id, user_id)[1]
    
    pro_sells = db.select_sells_product(user_id, user_id)
        
    pro_dict = {}
    pro_text =     ""
    raqam = 0
    narx = 0
    
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
            # print(pro_dict)
            # print(product)
            
            pro_text += f"{raqam}. id: {product[0]} - {product[1]}: \n \t  {product[3]} x {pro_dict[id]} ta  =  {pro_dict[id] * product[3]} so'm \n"
            narx += pro_dict[id] * product[3]
            
        pro_text += f"\n\nYetkazib berish: {yetkazish} so'm \n"
            
        matn = f"{name} siz tanlagan mahsulotlar ro'yxati \n\n"
        matn += pro_text
        
        matn += f"\n Jami: {narx+yetkazish} so'm"
        
        await call.message.answer(matn, reply_markup=savatcha_btn())


    else:
        matn = "Sizda hali buyurtmalar yo'q!\n"
        await call.message.answer(matn, reply_markup=main_btn)
    
    


@dp.callback_query_handler(state="find-pro3")
async def select_pro(call: CallbackQuery, state: FSMContext):
    # print(call.data)
    id = call.data[7:]
    if call.data[0:7]=="pocket:":
        db.add_sell_product(call.from_user.id, id)
        await call.answer(f"#id:{id} 🛍 savatga qo'shildi")
        await call.message.answer(f"✅ #id{id} \nMahsulot 🛍 savatga qo'shildi")
        
    elif call.data[0:7]=="collek:":
        # print("################################",id)
        try:
            db.add_sevimlilar(call.from_user.id, id)
            await call.message.answer(f"✅ #id{id} \nMahsulot ♥️ sevimlilarga qo'shildi")
            await call.answer(f"#id:{id} ♥️ sevimlilarga qo'shildi")
        except :
            await call.answer(f"#id:{id} ♥️ sevimlilarda mavjud")
        
    # await call.message.delete()
    
    
    # data = await state.get_data()
    # category = data.get("category")
    # subcategory = data.get("subcategory")

    # len_pro = db.select_product_category(category, subcategory)

    # products = len_pro[tr-1]
    products = db.select_product(id, id)
    
    print(products)
    

    matn = f"id: {products[0]}\n"
    matn += f"Name: {products[1]}\n"
    matn += f"Description: {products[2]}\n"

    
    user_id = call.from_user.id
    # pro_count = db.select_sells_product(user_id, user_id)
    sevimlilar = db.select_sevimlilar(user_id, user_id)

    pro_count = db.select_sells_product(user_id, user_id)
    
    
    pro_dict = {}
    narx = 0
    

    if pro_count:
        for i in pro_count:
            if i[2] in pro_dict:
                pro_dict[i[2]] = pro_dict[i[2]] + 1
            else:
                pro_dict[i[2]] = 1
            
        for tr in pro_dict:
            # raqam += 1
            
            product = db.select_product(tr, tr)
            narx += pro_dict[tr] * product[3]
    

    # await bot.edit_message_media(media=InputMedia(type='photo', media=products[6], caption = matn), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=show_products(len(len_pro), tr, "prev", "next", len(pro_count) ,products[0]))	
    try:
        
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=add_pocket(id,len(pro_count), products[3], products[1], len(sevimlilar), narx))
    except :
        pass
    await state.set_state("find-pro3")



@dp.message_handler(state="find-pro3")
async def send_ad_to_all(message: types.Message, state=FSMContext):
    if message.text.isdigit():
        
            
        pro_id = int(message.text)
        product_a = db.select_product(pro_id, pro_id)
        # print("sssssssssss-------:",product_a)
        if product_a:
            matn = f"id: {product_a[0]}\n"
            matn += f"Product Name: {product_a[1]}\n"
            matn += f"Caption: {product_a[2]}\n"

            user_id = message.from_user.id
            # pro_count = db.select_sells_product(user_id, user_id)
            sevimlilar = db.select_sevimlilar(user_id, user_id)
            
            pro_count = db.select_sells_product(user_id, user_id)
            # print("dddddddD------",pro_count)
            # print(pro_count)
            pro_dict = {}
            narx = 0
            
        
            if pro_count:
                for i in pro_count:
                    if i[2] in pro_dict:
                        pro_dict[i[2]] = pro_dict[i[2]] + 1
                    else:
                        pro_dict[i[2]] = 1
                    
                for id in pro_dict:
                    # raqam += 1
                    
                    product = db.select_product(id, id)
                    # print(":duct------",pro_dict)
                    # print(product)
                    
                    # pro_text += f"{raqam}. id: {product[0]} - {product[1]}: \n \t  {product[3]} x {pro_dict[id]} ta  =  {pro_dict[id] * product[3]} so'm \n"
                    narx += pro_dict[id] * product[3]
            
            # await message.reply(matn, reply_markup=admin_main_btn)
            print(pro_id)
            try:
                await bot.send_animation(chat_id=message.chat.id, animation=product_a[6], caption=matn , reply_markup=add_pocket(pro_id,len(pro_count), product_a[3], product_a[1], len(sevimlilar), narx)) 
                
            except :
                
                await bot.send_photo(chat_id=message.chat.id, photo=product_a[6], caption=matn , reply_markup=add_pocket(pro_id,len(pro_count), product_a[3], product_a[1], len(sevimlilar),narx))
    
            # await bot.send_photo(message.chat.id, user[6], matn , reply_markup=add_pocket(id,len(pro_count)))
            
            
        else:
            await message.answer("❌ Bu id dagi maxsulot topilmadi.", reply_markup=back_btn)
    else:
        await message.answer("❌ Faqat maxsulot id isini yuboring", reply_markup=back_btn)   
    await message.answer("Boshqa maxsulotni izlayotgan bo'lsangiz id sini yuboring:")
    # await state.finish()
    await state.set_state("find-pro3")
 ### mahsulotlarni izlash yakunlandi




    
@dp.message_handler(IsPrivate(), text="📞 Admin bilan aloqa",  state=None)
async def bot_start(message: types.Message, state=FSMContext):
    text = f"My Education Adminstratorlari bilan bog'lanish: \n\n"
    text += f"Telegram: @Jaloliddin_Mamatmusayev \n"
    text += f"Telefon: +998932977419\n"
    text += f"Telefon: +998332977419\n"
    text += f"Manzil: Toshkent, Yunusobod, Shaxriston, 10009"
    await message.answer(text)
    await bot.send_location(message.from_user.id, 41.353467, 69.288314)



@dp.message_handler(IsPrivate(), text="🌐 Ijtimoiy tarmoqlar",  state=None)
async def bot_start(message: types.Message, state=FSMContext):
    
    text = f"Bizni ijtimoiy tarmoqlarda kuzatib boring \n\n"
    text += f"<b>Telegram:</b> <a href='https://t.me/Jaloliddin_Mamatmusayev'>Jaloliddin_Mamatmusayev </a>\n"
    text += f"<b>Instagram:</b><a href='https://instagram.com/jaloliddin_1006'> jaloliddin_1006</a>\n"
    text += f"<b>You Tube:</b> JaloliddinMamatmusayev\n"
    await message.answer(text)




###########  sevimlilar bolimi
global my_tr
my_tr = 0
@dp.message_handler(text="♥️ Sevimlilar", state=None)
async def sevimlilar(message: types.Message, state=FSMContext):
    my_tr = 0
    user_id = message.from_user.id
    my_products = db.select_sevimlilar(user_id, user_id)
    if my_products:
        await message.answer("Sizning yoqtirgan mahsulotlaringiz", reply_markup=ReplyKeyboardRemove())
    
        i = my_products[my_tr]
        product = db.select_product(i[1], i[1])
        
        # for id in pro_dict:
        # raqam += 1
        
        # product = db.select_product(id, id)
        # print(pro_dict)
        # print(product)
        
        matn = f"id: {product[0]}\n"
        matn += f"<b>Name: {product[1]}</b>\n"
        matn += f"Description: {product[2]}\n"
        
        
        
        pro_count = db.select_sells_product(user_id, user_id)
        
        pro_dict = {}
        narx = 0
        
        if pro_count:
            for i in pro_count:
                if i[2] in pro_dict:
                    pro_dict[i[2]] = pro_dict[i[2]] + 1
                else:
                    pro_dict[i[2]] = 1
                
            for id in pro_dict:
                # raqam += 1
                
                producta = db.select_product(id, id)
                # print(pro_dict)
                # print(product)
                
                # pro_text += f"{raqam}. id: {product[0]} - {product[1]}: \n \t  {product[3]} x {pro_dict[id]} ta  =  {pro_dict[id] * product[3]} so'm \n"
                narx += pro_dict[id] * producta[3]

        try:
            await bot.send_animation(chat_id=message.chat.id, animation=product[6], caption=matn, reply_markup=show_like_products(len(my_products), my_tr+1, len(pro_count), product[0], product[3], product[1], narx))
            
        except :
            await bot.send_photo(message.chat.id, product[6], matn, reply_markup=show_like_products(len(my_products), my_tr+1, len(pro_count), product[0], product[3], product[1], narx))

        #     pro_text += f"{raqam}. id: {product[0]} - {product[1]}: \n \t  {product[3]} x {pro_dict[id]} ta  =  {pro_dict[id] * product[3]} so'm \n"
        #     narx += pro_dict[id] * product[3]
        # pro_text += f"\nJami: {narx}"
        await state.set_state("likes-next")
        # print(product)
    else:
        await message.reply("Siz tanlangan maxsulotlar yo'q", reply_markup=main_btn)


@dp.message_handler(IsPrivate(), text="/start",  state="likes-next")
async def bot_start(message: types.Message, state=FSMContext):
    await message.delete()
    await message.answer(f"""Assalomu alaykum {message.from_user.full_name}. Sizni bu yerda ko'rib turganimizdan hursandmiz.""", reply_markup=main_btn)
    await state.finish()


@dp.callback_query_handler(text="back_gr",  state="likes-next")
async def select_pro(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
     
    await call.message.answer(f"Bosh sahifa", reply_markup=main_btn)
    await state.finish()
    
    
    

@dp.callback_query_handler(text="next", state="likes-next")
async def select_pro(call: CallbackQuery, state: FSMContext):
    global my_tr
    my_tr += 1
    user_id = call.from_user.id
    my_products = db.select_sevimlilar(user_id, user_id)
    
    if len(my_products)>=my_tr+1:
        
            
        i = my_products[my_tr]
        product = db.select_product(i[1], i[1])
        
        matn = f"id: {product[0]}\n"
        matn += f"<b>Name: {product[1]}</b>\n"
        matn += f"Description: {product[2]}\n"
        pro_count = db.select_sells_product(user_id, user_id)
        
        pro_dict = {}
        narx = 0
        
    
        if pro_count:
            for i in pro_count:
                if i[2] in pro_dict:
                    pro_dict[i[2]] = pro_dict[i[2]] + 1
                else:
                    pro_dict[i[2]] = 1
                
            for id in pro_dict:
                # raqam += 1
                
                producta = db.select_product(id, id)
                # print(pro_dict)
                # print(product)
                
                # pro_text += f"{raqam}. id: {product[0]} - {product[1]}: \n \t  {product[3]} x {pro_dict[id]} ta  =  {pro_dict[id] * product[3]} so'm \n"
                narx += pro_dict[id] * producta[3]
        await bot.edit_message_media(media=InputMedia(type='photo', media=product[6], caption = matn), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=show_like_products(len(my_products), my_tr+1, len(pro_count), product[0], product[3], product[1], narx))	
    else:
        await call.answer("Bu oxirgi mahsulot")

        my_tr -= 1

    await state.set_state("likes-next")


        # pro_count = db.select_sells_product(user_id, user_id)



@dp.callback_query_handler(text="prev", state="likes-next")
async def select_pro(call: CallbackQuery, state: FSMContext):
    global my_tr
    my_tr -= 1
    user_id = call.from_user.id
    my_products = db.select_sevimlilar(user_id, user_id)
    
    if 0 < my_tr+1:
        
            
        i = my_products[my_tr]
        product = db.select_product(i[1], i[1])
        
        matn = f"id: {product[0]}\n"
        matn += f"<b>Name: {product[1]}</b>\n"
        matn += f"Description: {product[2]}\n"
        pro_count = db.select_sells_product(user_id, user_id)
        
        pro_dict = {}
        narx = 0
        
    
        if pro_count:
            for i in pro_count:
                if i[2] in pro_dict:
                    pro_dict[i[2]] = pro_dict[i[2]] + 1
                else:
                    pro_dict[i[2]] = 1
                
            for id in pro_dict:
                # raqam += 1
                
                producta = db.select_product(id, id)
                # print(pro_dict)
                # print(product)
                
                # pro_text += f"{raqam}. id: {product[0]} - {product[1]}: \n \t  {product[3]} x {pro_dict[id]} ta  =  {pro_dict[id] * product[3]} so'm \n"
                narx += pro_dict[id] * producta[3]
        
        await bot.edit_message_media(media=InputMedia(type='photo', media=product[6], caption = matn), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=show_like_products(len(my_products), my_tr+1, len(pro_count), product[0], product[3], product[1], narx))	
    else:
        await call.answer("Bu birinchi mahsulot")

        my_tr += 1

    await state.set_state("likes-next")

    # await call.message.delete()

@dp.callback_query_handler(text="place", state="likes-next")
async def select_pro(call: CallbackQuery, state: FSMContext):

    await call.answer(f"Mahsulotlar soni")
    await state.set_state("likes-next")



@dp.callback_query_handler(text="payme", state="likes-next")
async def select_pro(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.finish()
    await call.message.answer("Sizning savatchangizdagi mahsulotlar", reply_markup=main_btn)
    user_id = call.from_user.id
    
    name = db.select_user(user_id, user_id)[1]
    
    pro_sells = db.select_sells_product(user_id, user_id)
        
    pro_dict = {}
    pro_text =     ""
    raqam = 0
    narx = 0
    
 
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
        
        await call.message.answer(matn, reply_markup=savatcha_btn())


    else:
        matn = "Siz hali buyurtmalar yo'q!\n"
        await call.message.answer(matn, reply_markup=main_btn)
        
    

@dp.callback_query_handler( state="likes-next")
async def select_pro(call: CallbackQuery, state: FSMContext):
    pro_id = call.data[7:]
    user_id = call.from_user.id
    if call.data[0:7]=="pocket:":
        db.add_sell_product(call.from_user.id, pro_id)
    # db.add_sell_product(call.from_user.id, pro_id)
        
        await call.answer(f"#id:{pro_id} 🛍 savatga qo'shildi")
    elif call.data[0:7]=="delete:":
        # print("################################",id)
        db.delete_sevimlilar(user_id, pro_id)
        await call.answer(f"#id:{pro_id} 💔 sevimlilardan o'chirildi")
        
        
    my_products = db.select_sevimlilar(user_id, user_id)
    
    if 0 < my_tr:
        
            
        i = my_products[my_tr-1]
        print(my_tr)
        product = db.select_product(i[1], i[1])
        
        matn = f"id: {product[0]}\n"
        matn += f"<b>Name: {product[1]}</b>\n"
        matn += f"Description: {product[2]}\n"
        pro_count = db.select_sells_product(user_id, user_id)
        
        pro_dict = {}
        narx = 0
        

        if pro_count:
            for i in pro_count:
                if i[2] in pro_dict:
                    pro_dict[i[2]] = pro_dict[i[2]] + 1
                else:
                    pro_dict[i[2]] = 1
                
            for id in pro_dict:
                # raqam += 1
                
                producta = db.select_product(id, id)
                # print(pro_dict)
                # print(product)
                
                # pro_text += f"{raqam}. id: {product[0]} - {product[1]}: \n \t  {product[3]} x {pro_dict[id]} ta  =  {pro_dict[id] * product[3]} so'm \n"
                narx += pro_dict[id] * producta[3]
        
        await bot.edit_message_media(media=InputMedia(type='photo', media=product[6], caption = matn), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=show_like_products(len(my_products), my_tr, len(pro_count), product[0], product[3], product[1], narx))	
    else:
        await call.message.delete()
        await call.message.answer("Sizda sevimli xabarlar qolmadi", reply_markup=main_btn)
        await call.answer("Sizda sevimli xabarlar qolmadi")

    #     my_tr += 1

    await state.set_state("likes-next")
