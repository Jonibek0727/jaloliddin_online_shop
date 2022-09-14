from aiogram import types
from aiogram.types import LabeledPrice
# from handlers.users.payme_page import kuser_id
from utils.misc.product import Product
from loader import dp, bot, db
import sqlite3

# try:
#     sell = db.select_sells_product_check(kuser_id, kuser_id)
#     label = sell[2]
#     price = sell[3]
# except print(0):
narx=0
prices = []
print(prices, "##################################")


products_ = Product(
    title="Mahsulotlar uchun masofaviy to'lov",
    description="💵 Mahsulotlarni xarid qilish uchun quidagi tugmani bosing va onlayn to'lovni amalga oshiring.\n Bu onlayn to'lov xavfsiz va bunda siz hech qanday ma'lumotlaringizni yo'qotmaysiz.",
    currency="UZS",
    
    prices=prices,

    start_parameter="create_invoice_book_",
    photo_url='https://image.similarpng.com/very-thumbnail/2020/12/Online-payment-concept-Illustration-on-transparent-background-PNG.png',
    photo_width=1080,
    photo_height=1080,
    # photo_size=800,
    need_name=True,
    need_phone_number=True,
    need_shipping_address=True, # foydalanuvchi manzilini kiritishi shart
    is_flexible=True,
)

async def funci(user_id=None):
    try:
        
        
        # global prices
        if prices:
            print("--------1---------\n",prices)
            
            # prices = []
            print("--------2---------\n",prices)
        
        
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
            
            pro_text = f"{product[1]} - {pro_dict[id]} ta  \n"
            narx += pro_dict[id]*product[3]
            prices.append(LabeledPrice(label=pro_text, amount=pro_dict[id]*product[3]*100))
        
            
        prices.append(LabeledPrice(label="Yetkazib berish (7 kun)", amount=899900))
        
    #     global products_
    #     products_ = Product(
    #     title="Mahsulotlar uchun masofaviy to'lov",
    #     description="💵 Mahsulotlarni xarid qilish uchun quidagi tugmani bosing va onlayn to'lovni amalga oshiring.\n Bu onlayn to'lov xavfsiz va bunda siz hech qanday ma'lumotlaringizni yo'qotmaysiz.",
    #     currency="UZS",
        
    #     prices=prices,

    #     start_parameter="create_invoice_book_",
    #     photo_url='https://www.pngall.com/wp-content/uploads/5/Online-Payment-PNG-Photo.png',
    #     photo_width=1080,
    #     photo_height=1080,
    #     # photo_size=800,
    #     need_name=True,
    #     need_phone_number=True,
    #     need_shipping_address=True, # foydalanuvchi manzilini kiritishi shart
    #     is_flexible=True,
    # )
    except :
        print("xatooooooooo xxxxxxxxx")
print("--------3---------\n",prices)
    
     




REGULAR_SHIPPING = types.ShippingOption(
    id='post_reg',
    title="Fargo (3 kun). Maxsus quti bilan",
    prices=[
        LabeledPrice(
            'Maxsus quti', 599900),
        LabeledPrice(
            '3 ish kunida yetkazish', 899900),
    ]
)
FAST_SHIPPING = types.ShippingOption(
    id='post_fast',
    title='Express pochta (1 kun)',
    prices=[
        LabeledPrice(
            '1 kunda yetkazish', 1299900),
    ]
)

PICKUP_SHIPPING = types.ShippingOption(
    id='pickup',
    title="Do'kondan olib ketish",
    prices=[
        LabeledPrice("Yetkazib berishsiz", -899900)
    ])

