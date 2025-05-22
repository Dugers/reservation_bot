from aiogram import Router

from .welcome import welcome_router

handlers_router = Router()

routers = [
    welcome_router
]
if (routers):
    handlers_router.include_routers(*routers)