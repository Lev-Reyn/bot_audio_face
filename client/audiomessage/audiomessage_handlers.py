from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp
from aiogram import types, Dispatcher
from pathlib import Path
from aiogram.dispatcher.filters import Text
from client.audiomessage.convert import audio2wav
import os
from database import databasefunc

async def handle_file(file: types.File, file_name: str, path: str, bot):
    import os

    # checking if the directory demo_folder2
    # exist or not.
    if not os.path.isdir(path):
        # if the demo_folder2 directory is
        # not present then create it.
        os.makedirs(path)

    await bot.download_file(file_path=file.file_path, destination=f"{path}/{file_name}")
    audio2wav(audio_path=f"{path}/{file_name}", output_name=f"{path}/{file_name.split('.')[0]}")


# @dp.message_handler(content_types=[types.ContentType.VOICE])
async def voice_message_handler(message: types.Message):
    """срабатывает при получении ГС"""
    voice = await message.voice.get_file()
    path = f"database/audio/{message.from_user.id}user"

    try:  # узнаём номер ГС
        num_voice = len(os.listdir(f"database/audio/{message.from_user.id}user")) // 2
    except FileNotFoundError:
        num_voice = 0
    name_voice = f'audio_message_{num_voice}'  # названия под которым будет храниться ГС
    databasefunc.add_voice(name_column=name_voice, path=path + '/' + name_voice, telegramid=message.from_user.id)

    await handle_file(file=voice, file_name=f"{name_voice}.ogg", path=path, bot=message.bot)


def register_handlers_client_audiomessage(dp: Dispatcher):
    dp.register_message_handler(voice_message_handler, content_types=[types.ContentType.VOICE])
