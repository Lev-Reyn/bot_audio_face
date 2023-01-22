from create_bot import dp
from aiogram import types, Dispatcher
from database import databasefunc


# @dp.message_handler(commands=['get_data'])
async def get_data_process_command(message: types.Message):
    """получить csv файлик из БД"""
    databasefunc.mysql_in_csv('audio')

    doc = open('database/data/data_audio.csv', 'rb')
    await message.reply_document(doc)
    databasefunc.mysql_in_csv('photo')
    doc = open('database/data/data_photo.csv', 'rb')
    await message.reply_document(doc)


def register_handlers_admin_get_data(dp: Dispatcher):
    dp.register_message_handler(get_data_process_command, commands=['get_data'])
