from aiogram.utils import executor
from create_bot import dp
from client.audiomessage import audiomessage_handlers
from client.facemessage import facemessage_handlers
from client.begin import begin
from database import databasefunc
import asyncio


async def on_start(_):
    print('Bot is online')
    databasefunc.connection_with_mariadb()


# регистрируем хендлеры
audiomessage_handlers.register_handlers_client_audiomessage(dp)
begin.register_handlers_client_begin(dp)
facemessage_handlers.register_handlers_client_facemessage(dp)

executor.start_polling(dp, skip_updates=False, on_startup=on_start)


# исправить ошибку при добавдляении пути в БД
