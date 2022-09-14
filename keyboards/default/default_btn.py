from aiogram.types import ReplyKeyboardMarkup, KeyboardButton




phone_num = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📲 Telefon raqamimni yuborish",request_contact=True),           
        ],
    ],
    resize_keyboard=True
)

back_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔙 Ortga"),           
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Ortga qaytish uchun bosing"
    
)


maktab_ichi = ReplyKeyboardMarkup(
    keyboard=[
        [
           KeyboardButton(text="Bukletlar"),  
            KeyboardButton(text="Did. Materiallar"),   
        ],
        [         
            KeyboardButton(text="Suratlar"),   
            KeyboardButton(text="Lepbuklar"),   
    ],
          [
           KeyboardButton(text="Plakatlar"), 
           KeyboardButton(text="Bezak(оформление)"), 
          ],
          [          
            KeyboardButton(text="Maska(niqob)"),   
            KeyboardButton(text="Maket va o'yinlar"),   
    ],
           [
           KeyboardButton(text="Hujjatlar"), 
            
          ],
            [
           KeyboardButton(text="🔙 Ortga"), 
          
          ]
              ],
    resize_keyboard=True,
    input_field_placeholder="Guruhni tanlang"
    
)


bogcha_ichi = ReplyKeyboardMarkup(
    keyboard=[
        [
           KeyboardButton(text="Bukletlar"),  
            KeyboardButton(text="Did. Materiallar"),   
        ],
        [         
            KeyboardButton(text="Suratlar"),   
            KeyboardButton(text="Lepbuklar"),   
    ],
          [
           KeyboardButton(text="Plakatlar"), 
           KeyboardButton(text="Bezak(оформление)"), 
          ],
          [          
            KeyboardButton(text="Maska(niqob)"),   
            KeyboardButton(text="Maket va o'yinlar"),   
    ],
           [
           KeyboardButton(text="Hujjatlar"), 
            
          ],
            [
           KeyboardButton(text="🔙 Ortga"), 
          
          ]
              ],
    resize_keyboard=True,
    input_field_placeholder="Guruhni tanlang"
    
)


main_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
           KeyboardButton(text="Bog'cha uchun"),           
            KeyboardButton(text="Maktab uchun"),   
    ],
        [
            KeyboardButton(text="🔎 Mahsulotni izlash"),   
            
        ],
             [
           KeyboardButton(text="♥️ Sevimlilar"),           
            KeyboardButton(text="🛍 Savat"),   
    ],
            
             [
           KeyboardButton(text="📞 Admin bilan aloqa"),           
            KeyboardButton(text="🌐 Ijtimoiy tarmoqlar"),   
    ],
              [
           KeyboardButton(text="⚙️ Sozlamalar"),           
                 ],
     
              ],
    resize_keyboard=True,
    input_field_placeholder="Bo'limni tanlang",
    one_time_keyboard=True
    
)

user_settings =  ReplyKeyboardMarkup(
    keyboard=[
        [
           KeyboardButton(text="👤 Shaxsiy ma'lumotlarni"),  
           KeyboardButton(text="Tilni  🇺🇿 / 🇷🇺 "),          
  
    ],
          
          [
               KeyboardButton(text="🔙 Ortga"), 
          ]
              ],
    resize_keyboard=True,
    input_field_placeholder="Nimani o'zgartirmoqchisiz"
    
)

regions_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Tosheknt"),           
            KeyboardButton(text="Farg'ona"),            
        ],
          [
            KeyboardButton(text="Namangan"),           
            KeyboardButton(text="Andijon"),            
        ],
            [
            KeyboardButton(text="Sirdaryo"),           
            KeyboardButton(text="Jizzax"),            
        ],
              [
            KeyboardButton(text="Samarqand"),           
            KeyboardButton(text="Surxondaryo"),            
        ],
                [
            KeyboardButton(text="Qashqadaryo"),           
            KeyboardButton(text="Navoiy"),            
        ],
                  [
            KeyboardButton(text="Buqoro"),           
            KeyboardButton(text="Xorazm"),            
        ],
                    [
                  
            KeyboardButton(text="Qoraqalpog'iston Respublikasi"),            
        ],
       
    ],
    resize_keyboard=True,
    # one_time_keyboard=True,
    input_field_placeholder="Viloyatingizni tanlang"
)





admin_main_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
           KeyboardButton(text="🔍 Foydalanuvchini izlash"),           
            KeyboardButton(text="🔍 Mahsulotni izlash"),
    ],
          [
           KeyboardButton(text="Maktab uchun qo'shish"),           
           KeyboardButton(text="Bog'cha uchun qo'shish"),                     
    ],
           [
           KeyboardButton(text="📊 Statistika"),           
                             
    ]
              ],
    resize_keyboard=True,
    input_field_placeholder="Bo'limni tanlang"
    
)



admin_edit_pro_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
           KeyboardButton(text="🖋 Edit Name"),           
            KeyboardButton(text="📝 Edit Description"),
    ],
          [
           KeyboardButton(text="💵 Change Price"),           
           KeyboardButton(text="🖼 Change Photo"),                     
    ],
           [
           KeyboardButton(text="🔙 Back"),           
                             
    ]
              ],
    resize_keyboard=True,
    input_field_placeholder="What do you do?"
    
)

