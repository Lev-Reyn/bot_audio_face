from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp
from aiogram import types, Dispatcher
from pathlib import Path
from aiogram.dispatcher.filters import Text
from client.audiomessage.convert import audio2wav
import os
from database import databasefunc
from client.facemessage.facefind import Face



# @dp.message_handler(content_types=[types.ContentType.PHOTO])
async def photo_message_handler(message: types.Message):
    """срабатывает при получении фото"""
    path = 'database/test_photo'
    if not os.path.isdir(path):
        # if the demo_folder2 directory is
        # not present then create it.
        os.makedirs(path)

    num_photo = len(os.listdir(path))
    path_now = f'{path}/photo_{num_photo}.jpg'
    await message.photo[-1].download(path_now)

    if Face().download_photo_if_face(path_now=path_now, telegram_id=message.from_user.id, message=message):
        await message.reply('Лицо обнаружено, фотография добавлена')
    else:
        await message.reply('Лица не обнаружено :(')


def register_handlers_client_facemessage(dp: Dispatcher):
    dp.register_message_handler(photo_message_handler, content_types=[types.ContentType.PHOTO])
