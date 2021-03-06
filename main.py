"""
Main running module for bot.

Created on 03.03.2021

@author: Ruslan Dolovanyuk

"""

import asyncio
import pickle
import random

from aiogram import executor
from aiogram import types

from bot import bot, dp

import loader


class Compliments:
    data = None


class Languages:
    supported = None
    current = None


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    name = ''
    if message.from_user.username is not None:
        name = message.from_user.username
    menu_keyboard = await get_menu_keyboard()
    await message.answer(local('phrases', 'start').format(name), reply_markup=menu_keyboard, parse_mode="HTML")


@dp.message_handler(content_types=types.ContentTypes.ANY)
async def cmd_menu(message: types.Message):
    cmd = message.text
    await message.delete()
    if local('btn', 'want') == cmd:
        text = get_compliments()
        await message.answer(text, parse_mode="HTML")


async def get_menu_keyboard():
    menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, selective=True)
    menu_keyboard.add(types.KeyboardButton(local('btn', 'want')))
    return menu_keyboard


def get_compliments():
    return random.choice(Compliments.data)


def local(section, phrase):
    return Languages.current[section].get(phrase, '')


def load_language():
    with open('languages.dat', 'rb') as lang_file:
        data = pickle.load(lang_file)
        Languages.supported = data['languages']
        Languages.current = data[list(Languages.supported.keys())[0]]


def run():
    load_language()
    if Compliments.data is None:
        result = []
        dp.loop.run_until_complete(loader.worker(result))
        Compliments.data = result
        random.seed()
        random.shuffle(Compliments.data)
    executor.start_polling(dp, skip_updates=True)


if '__main__' == __name__:
    run()
