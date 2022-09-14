import asyncio

from aiogram import types, utils
from aiogram.types import ReplyKeyboardRemove, CallbackQuery
from keyboards.default.default_btn import admin_main_btn, maktab_ichi, back_btn, admin_edit_pro_btn, bogcha_ichi
from keyboards.inline.inline_btn import deleting, adding_pro
from data.config import ADMINS
from loader import dp, db, bot
from aiogram.dispatcher import FSMContext
from states.reg_state import products
from datetime import datetime

@dp.message_handler(text="/allusers", user_id=ADMINS)
async def get_all_users(message: types.Message):
    try:
        users = len(db.select_all_users())
        
    except Exception as e:
        users = 0
    await message.answer(f"Botdan fodyalanuvchilar soni: {users}")



## foydalanuvchini izlash
@dp.message_handler(text="🔍 Foydalanuvchini izlash", user_id=ADMINS, state=None)
async def send_ad_to_all(message: types.Message, state=FSMContext):
    await message.answer("Izlayotgan foydalanuvchingizni id sini yuboring:", reply_markup=ReplyKeyboardRemove())
    await state.set_state("find-user")



@dp.message_handler(text="🔙 Ortga",state="find-user")
async def send_ad_to_all(message: types.Message, state=FSMContext):
    await message.answer("Bosh sahifa", reply_markup=admin_main_btn)
    await state.finish()
   
   
@dp.message_handler(state="find-user")
async def send_ad_to_all(message: types.Message, state=FSMContext):
    id = int(message.text)
    user = db.select_user(id, id)
    checks = db.select_sells_product_check(id, id)
    print(checks)
    if user:
        matn = f"id: {user[0]}\n"
        matn += f"Full Name: {user[1]}\n"
        matn += f"Phone: {user[2]}\n"
        matn += f"Address: {user[3]}\n"
        matn += f"Start: {user[7]}\n"
        sells=""
        try:
            sells = f"\n{checks[3]}"
            sells += f"{checks[2]}\n"
            sells += f"Xarid vaqti: {checks[4]}\n"
        
        except :
            pass
        
        await message.reply(matn+sells, reply_markup=back_btn)
    else:
        await message.answer("❌ Topilmadi.", reply_markup=back_btn)
    
    await message.answer("Izlayotgan foydalanuvchining id sini yuboring:")
    await state.set_state("find-user")
 
 ##################  foydalanuvchini izlash yakunlandi #############
 
 
## maxsulot qo'shish
@dp.message_handler(text="Maktab uchun qo'shish", user_id=ADMINS, state=None)
async def send_ad_all(message: types.Message, state=FSMContext):
    
    category = "maktab"

    await state.update_data(
        {"category":category}
    )
    await message.answer("Qaysi guruhga qo'shasiz?", reply_markup=maktab_ichi)
    await products.subcategory.set()
    
@dp.message_handler(text="Bog'cha uchun qo'shish", user_id=ADMINS, state=None)
async def send_ad_all(message: types.Message, state=FSMContext):
    
    category = "bogcha"

    await state.update_data(
        {"category":category}
    )
    await message.answer("Qaysi guruhga qo'shasiz?", reply_markup=bogcha_ichi)
    await products.subcategory.set()


@dp.message_handler(text="🔙 Ortga",state=products.subcategory)
async def send_ad_to_all(message: types.Message, state=FSMContext):
    await message.answer("Bosh sahifa", reply_markup=admin_main_btn)
    await state.finish()
    
    
@dp.message_handler(user_id=ADMINS, state=products.subcategory)
async def send_ad_all(message: types.Message, state=FSMContext):
    if message.text == "Bukletlar":
        subcategory = "bukletlar"
    elif message.text == "Did. Materiallar":
        subcategory = "materiallar"
    elif message.text == "Suratlar":
        subcategory = "suratlar"
    elif message.text == "Lepbuklar":
        subcategory = "lepbuklar"
    elif message.text == "Plakatlar":
        subcategory = "plakatlar"
    elif message.text == "Bezak(оформление)":
        subcategory = "bezak"
    elif message.text == "Maska(niqob)":
        subcategory = "maska"
    elif message.text == "Maket va o'yinlar":
        subcategory = "maket"
    elif message.text == "Hujjatlar":
        subcategory = "hujjatlar"

    await state.update_data(
        {"subcategory":subcategory}
    )
    await message.answer("Maxsulot nomini kiriting", reply_markup=ReplyKeyboardRemove())
    await products.name.set()


@dp.message_handler(user_id=ADMINS, state=products.name)
async def send_ad_all(message: types.Message, state=FSMContext):
    name = message.text

    await state.update_data(
        {"name":name}
    )
    await message.answer("Maxsulot haqida qisqacha ma'lumot kiriting")
    await products.caption.set()
    


@dp.message_handler(user_id=ADMINS, state=products.price)
async def send_ad_all(message: types.Message, state=FSMContext):
    price = message.text
    if price.isdigit():

        await state.update_data(
            {"price":price}
        )
        await message.answer("Maxsulot rasmi( rasm yoki gif linki)ni yuboring")
        await products.photo.set()
    else:
        await message.answer("Maxsulot narxini kiriting(so'm)\n<i>(faqat sonlarda) \n\tMasalan: 5600</i>")
        await products.price.set()


@dp.message_handler(user_id=ADMINS, state=products.caption)
async def send_ad_all(message: types.Message, state=FSMContext):
    caption = message.text

    await state.update_data(
        {"caption":caption}
    )
    await message.answer("Maxsulot narxini kiriting(so'm)\n<i>(faqat sonlarda) \n\tMasalan: 5600</i>")
    await products.price.set()
    


@dp.message_handler(user_id=ADMINS, state=products.photo, content_types=['photo', 'text'])
async def send_ad_all(message: types.Message, state=FSMContext):
    
    if message.photo:
        photo = message.photo[0].file_id
    elif message.text:
        photo = message.text
        
    await state.update_data(
        {"photo":photo}
    )
    
    
    data = await state.get_data()
    name = data.get("name")
    caption = data.get("caption")
    price = data.get("price")
    photo = data.get("photo")
    # category = data.get("category")
    # subcategory = data.get("subcategory")
    today = datetime.now().date()
    
    
  
    matn = f"Product Name: {name}\n"
    matn += f"Caption: {caption}\n"
    matn += f"Price: {price} sum\n"
    # matn += f"Category: {category}\n"
    # matn += f"Subcategory: {subcategory}\n"
   

    # await message.reply(matn, reply_markup=admin_main_btn)
    if message.text:
        await bot.send_animation(chat_id = message.chat.id, animation=photo, caption=matn)
    else:
        await bot.send_photo(message.chat.id, photo, matn )
    
    await message.answer("Ma'lumotlar barchasi to'g'rimi? ", reply_markup=adding_pro)
    await products.finish.set()
    
    
@dp.callback_query_handler(text="yes",  state= products.finish)
async def select_pro(call: CallbackQuery, state:FSMContext):
    await call.message.delete()
    
    data = await state.get_data()
    name = data.get("name")
    caption = data.get("caption")
    price = data.get("price")
    photo = data.get("photo")
    category = data.get("category")
    subcategory = data.get("subcategory")
    today = datetime.now().date()
    
    try:
        db.add_product(name, caption, price, category, subcategory, photo, today)
        pro = db.select_all_product()[-1][0]
        await call.message.answer(f"#id: {pro}  - - {name}\n\n✅ Bazaga qo'shildi", reply_markup=admin_main_btn)
       
            
    except Exception as err:
        print("maxsulot qo'shishda xatolik>>>>>", err)
    await state.finish()    
       
@dp.callback_query_handler(text="no",  state= products.finish)
async def select_pro(call: CallbackQuery, state:FSMContext):
    await call.message.delete() 
    await call.message.answer("❌ Bekor qilindi", reply_markup=admin_main_btn)
    await state.finish()    

@dp.message_handler(user_id=ADMINS, state=products.photo)
async def send_ad_all(message: types.Message, state=FSMContext):
  
    await message.answer("Maxsulot rasmini jo'nating")
    await products.photo.set()
    
################### mahsulotlar qo'shish yakunlandi ############



## maxsulotni izlash ###
@dp.message_handler(text="🔍 Mahsulotni izlash", user_id=ADMINS, state=None)
async def send_ad_to_all(message: types.Message, state=FSMContext):
    await message.answer("Izlayotgan maxsulotingiz id sini yuboring:", reply_markup=back_btn)
    await state.set_data(
            {"i_d": "3"}
            
            )
        
    await state.set_state("find-pro")

    
@dp.callback_query_handler( state="find-pro")
async def select_pro(call: CallbackQuery, state:FSMContext):
    if call.data[0:5] == "edit:":
        pro_id = f"{call.data[5:]}"
        # await state.set_data(
        #     {"pro_id": "id"}
            
        #     )
        await state.set_data(
        {"id": pro_id}
    )
        
        # await call.message.delete()
        await call.message.edit_reply_markup()
        print("ishladi 1-", pro_id)
        await call.message.answer(f"#id: {call.data[5:]}\nUshbu mahsulotning nimasini o'zgartirmoqchisiz?", reply_markup=admin_edit_pro_btn)
        await state.set_state("change-pro-info")
        
    elif call.data[0:7] == "delete:":
        # await call.answer(show_alert="ok")
        
        # www = call.message.reply_markup.inline_keyboard[0][1]["callback_data"]
        # print(www)
        id = call.data[7:]
        await call.message.delete()
        db.delete_product(id, id)

        await call.message.answer(f"#id : {call.data}  -  maxsulot o'chirildi ✅",)
        await call.message.answer("Bosh sahifa", reply_markup=admin_main_btn)
        await state.finish()
    else:
        print("xatolik")


@dp.message_handler(text="🔙 Ortga",state="find-pro")
async def send_ad_to_all(message: types.Message, state=FSMContext):
    await message.answer("Bosh sahifa", reply_markup=admin_main_btn)
    await state.finish()
    
@dp.message_handler(state="find-pro")
async def send_ad_to_all(message: types.Message, state=FSMContext):
    id = int(message.text)
    
    user = db.select_product(id, id)
    if user:
        matn = f"id: {user[0]}\n"
        matn += f"Product Name: {user[1]}\n"
        matn += f"Caption: {user[2]}\n"
        matn += f"Price: {user[3]} sum\n"
        # matn += f"Category: {user[4]}\n"
        # matn += f"Subcategory: {user[5]}\n"
        # matn += f"Date: {user[7]}\n"
        
        # await message.reply(matn, reply_markup=admin_main_btn)
        try:
            await bot.send_animation(chat_id=message.chat.id, animation=user[6], caption=matn , reply_markup=deleting(id))
            
        except :
            
            await bot.send_photo(chat_id=message.chat.id, photo=user[6], caption=matn , reply_markup=deleting(id))
        
        
    else:
        await message.answer("❌ Topilmadi.", reply_markup=back_btn)
        
    await message.answer("Boshqa maxsulotni izlayotgan bo'lsangiz id sini yuboring:")
    await state.set_state("find-pro")
    
    
    
    
    
    


@dp.message_handler(text="🔙 Back",state="change-pro-info")
async def send_ad_to_all(message: types.Message, state=FSMContext):
    await message.answer("Bosh sahifa", reply_markup=admin_main_btn)
    await state.finish()
    

@dp.message_handler(text="🖋 Edit Name",state="change-pro-info")
async def send_ad_to_all(message: types.Message, state=FSMContext):
    # await message.answer("Bosh sahifa", reply_markup=admin_main_btn)
    print("ishladi edit name gacha")
    await state.update_data(
        {"progress": "name"}
    )
    # data = await state.get_data()
    # pro_id = data.get("pro_id")
    await message.reply("Mahsulotning yangi nomini kiriting:", reply_markup=ReplyKeyboardRemove())
    await state.set_state("change-info")


@dp.message_handler(text="📝 Edit Description",state="change-pro-info")
async def send_ad_to_all(message: types.Message, state=FSMContext):
    # await message.answer("Bosh sahifa", reply_markup=admin_main_btn)
    print("ishladi edit desc gacha")
    await state.set_data(
        {"progress": "desc"}
    )
    # data = await state.get_data()
    # pro_id = data.get("pro_id")
    await message.reply("Mahsulot haqida qisqacha ma'lumot kiriting:", reply_markup=ReplyKeyboardRemove())
    
    await state.set_state("change-info")


@dp.message_handler(text="💵 Change Price",state="change-pro-info")
async def send_ad_to_all(message: types.Message, state=FSMContext):
    # await message.answer("Bosh sahifa", reply_markup=admin_main_btn)
    print("ishladi edit name gacha")
    await state.set_data(
        {"progress": "price"}
    )
    # data = await state.get_data()
    # pro_id = data.get("pro_id")
    await message.reply("Mahsulotning yangi narxini kiriting:", reply_markup=ReplyKeyboardRemove())
    
    await state.set_state("change-info")


@dp.message_handler(text="🖼 Change Photo",state="change-pro-info")
async def send_ad_to_all(message: types.Message, state=FSMContext):
    # await message.answer("Bosh sahifa", reply_markup=admin_main_btn)
    print("ishladi edit name gacha")
    await state.set_data(
        {"progress": "photo"}
    )
    await message.reply("Mahsulotning yangi rasmi(gif yoki link) yuboring:", reply_markup=ReplyKeyboardRemove())
    await state.set_state("change-info")


@dp.message_handler(state="change-info", content_types=["photo", "text"])
async def send_ad_to_all(message: types.Message, state=FSMContext):
    # await message.answer("Bosh sahifa", reply_markup=admin_main_btn)
    print("ishladi edit name gacha")
    new = message.text
    data = await state.get_data()
    pro_id = data.get("id")
    # id = data.get("i_d")
    progress = data.get("progress")
    # a = data.values()
    # print("######", new)
    # print("######", id)
    # print("######", pro_id)
    # print("######", progress)
    # print("######", a)
    
    if progress == "name":
        db.edit_product_name(new, pro_id)
        await message.answer("✅ Mahsulot nomi muvaffaqiyatli o'zgartirildi", reply_markup=admin_edit_pro_btn)



    elif progress == "desc":
        db.edit_product_desc(new, pro_id)
        await message.answer("✅ Maxsulot haqidagi qisqacha ma'lumot  muvaffaqiyatli o'zgartirildi", reply_markup=admin_edit_pro_btn)
    elif progress == "price":
        db.edit_product_price(new, pro_id)
        await message.answer("✅ Mahsulot narxi muvaffaqiyatli o'zgartirildi", reply_markup=admin_edit_pro_btn)
    elif progress == "photo":
        db.edit_product_photo_url(new, pro_id)
        await message.answer("✅ Maxsulot rasmi muvaffaqiyatli o'zgartirildi", reply_markup=admin_edit_pro_btn)
    else:
        print("updateda xatolik")
    
    await state.set_state("change-pro-info")
    




 ### mahsulotlarni izlash yakunlandi


### statistika #########
@dp.message_handler(text="📊 Statistika", user_id=ADMINS)
async def static_all(message: types.Message):
    products = db.select_all_product()
    users = db.select_all_users()
    await message.answer(f"Botdan foydalanuvchilar soni: {len(users)}")
    await message.answer(f"Botdagi maxsulotlar soni: {len(products)}")
   







 
 
## reklama xizmati
@dp.message_handler(text="/reklama", user_id=ADMINS, state=None)
async def send_ad_to_all(message: types.Message, state=FSMContext):
    try:
        await message.answer("✅ Reklamani botga forward qiling. Siz forward qilgan reklama to'gridan to'g'ri barcha foydalanuchilarga yuboriladi. \n\n✅ Yoki xabar matnini kiriting: \n\n⚠️ Xabar yuborishni istamasangiz /bekor kamandasini kiriting.", reply_markup=ReplyKeyboardRemove())
        # print("1")
    except Exception as e:
        await message.answer("✅ Reklamani botga forward qiling. Siz forward qilgan reklama to'gridan to'g'ri barcha foydalanuchilarga yuboriladi. \n\n✅ Yoki xabar matnini kiriting: \n\n⚠️ Xabar yuborishni istamasangiz /bekor kamandasini kiriting.")
        # print("2")
        
    await state.set_state("send_users")



@dp.message_handler(state="send_users", text="/bekor")
async def send_ad_to_all(message: types.Message, state=FSMContext):
    await message.answer("❌ Bekor qilindi")
    await state.finish()
 


@dp.message_handler(state="send_users", content_types="text", is_forwarded=False)
async def send_ad_to_all(message: types.Message, state=FSMContext):
    await state.finish()
    bloklaganlar = 0
    jonlilar = 0

    users = db.select_all_users()
    # print(message)
    # print(message.forward_from_message_id)
    # print(message.forward_from.id)
    for user in users:
        user_id = user[0]
        # print(message.message_id)

        try:
            # await message.answer(user_id,  message.text ) 
            await bot.send_message(user_id, message.text) 
            # print(jonlilar)
            jonlilar += 1
            # print("user's msg")
        except utils.exceptions.BotBlocked as e:
            bloklaganlar += 1
            # print("blok")
            
        except:
            pass
        #     await message.forward(user_id, message.forward_from_chat.id, message.forward_from_message_id ) 
            # print("channel's msg")

        else:
            pass


        # print("yes")
        await asyncio.sleep(0.05)
    await message.answer("✅ Xabaringiz foydalanuvchilarga yetkazildi...")
    await message.answer(f"Jami foydalanuvchilar soni: {bloklaganlar+jonlilar}")
    await message.answer(f"Bloklagan foydalanuvchilar soni: {bloklaganlar}")
    await message.answer(f"Faol foydalanuvchilar soni: {jonlilar}")

 

@dp.message_handler(state="send_users", content_types="any", is_forwarded=True)
async def send_ad_to_all(message: types.Message, state=FSMContext):
    await state.finish()
  
    bloklaganlar = 0
    jonlilar = 0

    users = db.select_all_users()
    # print(message)
    # print(message.forward_from_message_id)
    # print(message.forward_from.id)
    for user in users:
        user_id = user[0]
        # print(message.message_id)

        try:
            await message.forward(user_id, message.forward_from.id, message.forward_from_message_id ) 
            # print("user's msg")
            jonlilar += 1

        except utils.exceptions.BotBlocked as e:
            # print("blok")
            bloklaganlar += 1

            # pass
        except:
            await message.forward(user_id, message.forward_from_chat.id, message.forward_from_message_id ) 
            # print("channel's msg")
            jonlilar += 1


        else:
            pass


        # print("yes")
        await asyncio.sleep(0.05)


    await message.answer("✅ Xabaringiz foydalanuvchilarga yetkazildi...")

    await message.answer(f"Jami foydalanuvchilar soni: {bloklaganlar+jonlilar}")
    await message.answer(f"Bloklagan foydalanuvchilar soni: {bloklaganlar}")
    await message.answer(f"Faol foydalanuvchilar soni: {jonlilar}")
