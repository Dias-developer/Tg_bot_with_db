from aiogram import Dispatcher, Bot
from dotenv import load_dotenv
import asyncio
from os import getenv
import logging

from handlers import router
from db import create_table
load_dotenv()
token = getenv("TOKEN")
dp = Dispatcher()

async def main():

    create_table()

    dp.include_router(router)
    bot = Bot(token=token)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print('Start...')
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Stop...')
