from create_bot import dp
from aiogram import types, Dispatcher
from database import databasefunc


# @dp.message_handler(commands=['start'])
async def start_process_command(message: types.Message):
    """запуск бота"""
    if not databasefunc.add_user(message.from_user.id, table='audio'):
        await message.reply(f'Ты уже есть в БД!')
        return
    databasefunc.add_user(message.from_user.id, table='photo')  # так же созда
    await message.reply(f'Привет {message.from_user.full_name} <b>бот / тестовое задания на специальность '
                        f'Data Collection Specialist (Junior Python Developer)</b>\nкоманды слева от клавиатуры')


# @dp.message_handler(commands=['help'])
async def help_process_command(message: types.Message):
    """описание бота"""
    await message.reply('Бот для тестового задания,\nсохраняет ГС и фото с лицами в отельные директории созданные под '
                        'каждого пользователя, информацию о пользователях сохраняет в mysql, с помощью /get_data можно'
                        ' получить csv файлы аудио и фото по пользователям')

def register_handlers_client_begin(dp: Dispatcher):
    dp.register_message_handler(start_process_command, commands=['start'])
    dp.register_message_handler(help_process_command, commands=['help'])
