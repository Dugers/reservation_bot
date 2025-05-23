from aiogram import Dispatcher, Bot
from aiogram_dialog import setup_dialogs
from aiogram.fsm.storage.memory import MemoryStorage

from reservation_bot.config import settings
from reservation_bot.dialogs import dialogs_router
from reservation_bot.handlers import handlers_router
from reservation_bot.middlewares import middlewares
from reservation_bot.di import container

storage = MemoryStorage()
bot = Bot(settings.bot.token)
dp = Dispatcher(storage=storage)

dp.include_router(handlers_router)
dp.include_router(dialogs_router)

for middleware in middlewares:
    dp.callback_query.outer_middleware(middleware)
    dp.message.outer_middleware(middleware)

setup_dialogs(dp)

async def run_bot():
    await container.init_resources()
    container.wire(
        packages=[
            "reservation_bot.dialogs"
        ]
    )
    await dp.start_polling(bot)