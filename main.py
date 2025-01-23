import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils import keyboard

import json


def init(config_path: str) -> (str):
    try:
        config = json.load(open(config_path))
        token = config["token"]
        return token

    except FileNotFoundError as e:
        print(f"bad filepath {config_path}")
        sys.exit(1)

    except json.decoder.JSONDecodeError as e:
        print(f"json parsing failed {e}")
        sys.exit(2)

    except Exception as e:
        print(f"unexpected error while parsing config {e}")
        sys.exit(-1)


TOKEN = init("config.json")
dp = Dispatcher()
MESSAGE = None

builder = keyboard.ReplyKeyboardBuilder()
builder.button(text='''📖What's included in PREMIUM subscription?''')
builder.button(text='❓How does it work?')
builder.button(text='📢Reviews')
builder.button(text='📊Stats')
builder.button(text='💳Price')
builder.adjust(1,1,1,2)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("a", reply_markup=builder.as_markup())


@dp.message(F.text.lower() == 'des шифрование')
async def des_encrypt(message: Message) -> None:
    try:
        global MESSAGE
        if MESSAGE is not None:
            global DES_KEY
            await message.answer(des.encrypt(DES_KEY, MESSAGE))
        else:
            await message.answer("Сначала отправьте текст")
    except Exception as e:
        await message.answer(f"Что-то пошло не так ({e})")



# мы получили параметры для бота с помощью init(), а затем запустили опрос, используя dispatcher,
# тогда для любого сообщения у нас есть несколько обработчиков для их обработки
async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())