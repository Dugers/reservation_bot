from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage

from reservation_bot.config import settings
from reservation_bot.dialogs import dialogs_router
from reservation_bot.handlers import handlers_router
from reservation_bot.middlewares import middlewares

storage = MemoryStorage()
bot = Bot(settings.bot.token)
dp = Dispatcher(storage=storage)

dp.include_router(handlers_router)
dp.include_router(dialogs_router)

for middleware in middlewares:
    dp.callback_query.outer_middleware(middleware)
    dp.message.outer_middleware(middleware)

async def run_bot():
    await dp.start_polling(bot)