from aiogram import executor
from dispatcher import dp
from file_api.http_server import download_file
from aiohttp import web
from aiohttp import streamer
import asyncio
import handlers

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
