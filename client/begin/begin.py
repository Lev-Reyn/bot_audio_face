from create_bot import dp
from aiogram import types, Dispatcher
from database import databasefunc


# @dp.message_handler(commands=['start'])
async def start_process_command(message: types.Message):
    """запуск бота"""
    if not databasefunc.add_user(message.from_user.id):
        await message.reply(f'Ты уже есть в БД!')
        return
    await message.reply(f'Привет {message.from_user.full_name} <b>бот / тестовое задания на специальность '
                        f'Data Collection Specialist (Junior Python Developer)</b>\nкоманды слева от клавиатуры')


def register_handlers_client_begin(dp: Dispatcher):
    dp.register_message_handler(start_process_command, commands=['start'])

