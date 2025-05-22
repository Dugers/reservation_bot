import asyncio
from functools import wraps
import logging

from reservation_bot import run_bot

def setup_and_run_bot(setup_function):
    @wraps(setup_function)
    def wrapper(*args, **kwargs):
        setup_function(*args, **kwargs)
        asyncio.run(run_bot())
    return wrapper

@setup_and_run_bot
def run_prod():
    logging.basicConfig(level=logging.INFO)
    logging.info("Start prod")

@setup_and_run_bot
def run_dev():
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Start dev")
