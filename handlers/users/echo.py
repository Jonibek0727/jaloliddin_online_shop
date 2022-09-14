from aiogram import types

from loader import dp, bot


# Echo bot
@dp.message_handler()
async def bot_echo(message: types.Message):
    await message.answer("Noto'g'ri buyruq")


@dp.message_handler(content_types=['photo', 'gif'])
async def scan_message(msg: types.Message):
    document_id = msg.photo[0].file_id
    # print(document_id)
    
    # await bot.send_photo(msg.chat.id, document_id, "rasm" )
   
    # file_info = await bot.get_file(document_id)
    # print(file_info)
    # print(f'file_id: {file_info.file_id}')
    # print(f'file_path: {file_info.file_path}')
    # print(f'file_size: {file_info.file_size}')
    # print(f'file_unique_id: {file_info.file_unique_id}')