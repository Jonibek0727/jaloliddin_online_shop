from loader import db
from utils.db_api.sqlite import Database


# from translate import Translator
# translator= Translator(from_lang="english",to_lang="russian")
# translation = translator.translate("home")
# print(translation)







def dbtest():
    # db.create_table_users()
    # db.create_table_reg_users()
    # db.create_table_products()
    # db.create_table_sells()
    # db.create_table_sell_products()
    # db.create_table_sevimlilar()


    
    # db.add_user(99893287, "Jaloliddin", "04/09/2022")
    # db.add_user(99897287, "Jaloliddin", "05/09/2022")
    # db.add_user(99993287, "Jaloliddin", "2/09/2022")
    # db.add_user(89897287, "Jaloliddin", "04/2/2022")
    # db.add_user(89893387, "Jaloliddin", "04/2/2021")
    
    
    
    # db.add_reg_user(id, name, phone, adress, lan, status, date_of_start)
    # db.add_reg_user(99888787, "name", "phone", "adress", "lan", 0, "date_of_start")
    # user = db.select_user(99895787)
    # print(user)
    
    # update user info
    # db.update_user_info("my name", "99893297419", "toshkent", 99888787)
    
    
    # db.update_user_lan("uz", 99888787)
    
    
    # user = db.select_user(99895287)
    # if user:
    #     print(user)
    # else:
    #     print("yoq")
        
    # db.add_product("name", "caption", 1800, "category", "sub category","photo_url", "date_of_start")
    
    
    # db.delete_product(2, 2)
    
    # products = db.select_all_product()
    # print(len(products))
    # print(products)
    
    # users = db.select_all_users()
    # print(len(users))


    select_pro = db.select_product_category("maktab", "katta")
    # print(select_pro)
    
    # db.add_sell_product(973108256, 9)
    # db.add_sell_product(973108254, 11)
    # db.add_sell_product(973108256, 10)
    # db.add_sell_product(973108256, 11)
    # db.add_sell_product(973108256, 9)
    # print("a")
    # pro_count = db.select_sells_product(973108256, 973108256)
    
    # print(len(pro_count))
    # for i in pro_count:
    #     print(i)
    
    
    # db.add_sells_products(973108256, "stol, ruchka, daftar", 150000, "22.05.2022", 0)

    # print(db.select_sells_product_check(973108256, 973108256))
    print(db.select_product(3, 3))
    # db.edit_product_name("Ifodali oqish", 3)
    print(db.select_product(3, 3))
    
    
    # db.add_sevimlilar(973108256, 8)
    # db.add_sell_product(973108256, 5)
    # db.delete_sells_product(973108256, 8)
    # db.delete_sells_all_product(973108256, 973108256)
dbtest()


 
# prices1 = []
# prices1.append(LabeledPrice(label="Kitob", amount=7000000))


# pro_dict = {8:3,6:1,12:1}
# pro_dict[8] += 1
# pro_dict[15] = 8


# for i in pro_dict:
#     print(i)
#     print(i, pro_dict[i])

# thisdict = {
#   "brand": "Ford",
#   "model": "Mustang",
#   "year": 1964
# }

# for i in thisdict:
#     print(i)

# a = "salom dunyo "
# b = a.split()
# print(b)
# c=0
# for i in a:
#     if i.isnumeric():
#         c+=1
        
        
# if not c:
#     print("son bor")






# {"message_id": 1190, 
#  "from": {"id": 5737425650, "is_bot": true, "first_name": "MyEducationBot", "username": "myeduinfobot"}, 
#  "chat": {"id": 973108256, "first_name": "𝕵𝖆𝖑𝖔𝖑𝖎𝖉�𝖎𝖓  ️️ ️ ️️💠", "username": "Jaloliddin_Mamatmusayev", "type": "private"}, 
#  "date": 1662575898, 
#  "ph  oto": [{"file_id": "AgACAgIAAxkDAAIEpmMY5RoQN2IFcvqU1V9knhanLyuCAAKmwTEb657BSD7Ff    fuql8lZvAQADAgADcwADKQQ", "file_unique_id": "AQADpsExG-uewUh4", "file_size": 505, "width": 90, "height": 30}, 
#              {"file_id": "AgACAgIAAxkDAAIEpmMY5RoQN2IFcvqU1V9knhanLyuCAAKmwTEb657BSD7Ffuql8lZvAQADAgADbQADKQQ", "file_unique_id": "AQADpsExG-uewUhy", "file_size": 3808, "width": 320, "height": 105}, 
#              {"file_id": "AgACAgIAAxkDAAIEpmMY5RoQN2IFcvqU1V9knhanLyuCAAKmwTEb657BSD7Ffuql8lZvAQADAgADeAADKQQ", "file_unique_id": "AQADpsExG-uewUh9", "file_size": 4431, "width": 400, "height": 131}], 
#  "caption": "id: 8\nProduct Name: qalam\nCaption: qora qalam\nPrice: 800 sum\nCategory: bogcha\nSubcategory: katta\nDate: 2022-09-07", 
#  "reply_markup": {
#      "inline_keyboard": [[{"text": "⬅️", "callback_data": "prev"}, 
#                           {"text": "1 / 2", "callback_ddata": "place"}, 
#                           {"text": "➡️", "callback_data": "next"}], 
#                          [{"text": "🗑 Savatga qo'shish", "callback _data": "8"}], 
#                          [{"text": "💴 To'lov qilish", "callback_data": "payme"}], 
#                          [{"text"": "🔙 Ortga", "callback_data": "back_gr"}]]}}




# [[<InlineKeyboardButton {"text": "⬅️", "callback_data": "prev"}>, 
#   <InlineKeyboardButton {"text": "1 / 2", "callback_data": "place"}>, 
#   <InlineKeyboardButton {"text": "➡️", "callback_ _data": "next"}>], 
#  [<InlineKeyboardButton {"text": "🗑 Savatga qo'shish", "callback_data": "8"}>], 
#  [< InlineKeyboardButton {"text": "💴 To'lov qilish", "callback_data": "payme"}>], 
#  [<InlineKeyboardButton {"text": "🔙 Ortga", "callback_data": "back_gr"}>]]





# {"id": "4179468138539923496", 
#  "from": {"id": 973108256, "is_bot": false, "first_name": "𝕵𝖆𝖑𝖔𝖑𝖎𝖉𝖉𝖎𝖓 ️️ ️ ️️💠", "username": "Jaloliddin_Mamatmusayev", "language_code": "en"}, 
#  "message": {"message_id": 1232, 
#              "from": {"id": 5737425650, 
#                       "is_bot": true, 
#                       "first_name": "MyEducationBot", 
#                       "username": "myeduinfobot"}, 
#              "chat": {"id": 973108256, 
#                       "first_name": "�𝖆𝖑𝖔𝖑𝖎𝖉𝖉𝖎𝖓  ️️ ️ ️️💠", 
#                       "username": "Jaloliddin_Mamatmusayev", 
#                       "type": "private"}, 
#              "date": 1662576582, 
#              "edit_date": 1662576586,
#              "photo": [{"file_id": "AgACAgIAAxkDAAIE0GMY58    8qZZlJts4mdFPi--NgQ534NAAKowTEb657BSMFafhJhVtGJAQADAgADcwADKQQ", 
#                         "file_unique_id": "AQADqMExG-uewUh4", 
#                         "file_size": 787, 
#                         "width": 90, 
#                         "height": 64}, 
#                        {"file_id": "AgACAgIAAxkDAAIE0GMY58qZZlJts4mdFPi--NgQ534NAAKowTEb657BSMFafhJhVtGJAQADAgADbQADKQQ", 
#                         "file_unique_id": "AQADqMExG-uewUhy", 
#                         "file_size": 2592, 
#                         "width": 176, 
#                         "height": 125}], 
#              "caption": "id: 9\nProduct Name: komputer\nCaption: stol komputeri\nPrice: 48000 sum\nCategory: bogcha\nSubcategory: katta\nDate: 2022-09-07", 
#              "reply_markup": {
#                  "inline_keyboard": [[{"text": "⬅️", "callback_daata": "prev"}, 
#                                       {"text": "2 / 2", "callback_data": "place"}, 
#                                       {"text": "➡️", "callback_data": "next"}], 
#                                      [{"text": "🗑 Savatga qo'shish", "callback_data": "9"}], 
#                                      [{"text": "💴 To'lov qilish", "callback_data": "payme"}], 
#                                      [{"text": "🔙 Ortga", "callback_data": "back_gr"}]]}}, 
# "chat_instance": "1487201462396582295", 
# "data": "9"}






b = "aa"
def funci(aa):
    global b
    b = aa
    
print(b)
funci(5)
print(b)


l = [b]
print(l)