"""
Init module for bot.

Created on 03.03.2021

@author: Ruslan Dolovanyuk

"""

import asyncio

from aiogram import Bot, Dispatcher

from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import API_TOKEN


bot = Bot(token=API_TOKEN)
storage = MemoryStorage()

dp = Dispatcher(bot, loop=asyncio.get_event_loop(), storage=storage)
