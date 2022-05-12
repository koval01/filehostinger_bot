from aiogram import types
from aiogram.types import ContentType
from dispatcher import dp
from file_api.extract_link import Extractor


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(msg: types.Message):
    await msg.reply(
        "Send me any file weighing up to 20 megabytes. The file can be any: photo, video, "
        "document, voice message, video note, gif, sticker... In reply, I will send you a"
        " link with direct access to this file / media content"
    )


@dp.message_handler(content_types=ContentType.PHOTO)
async def take_photo(msg: types.Message):
    await msg.reply(Extractor(msg, photo=True).build_link)


@dp.message_handler(content_types=[
    ContentType.STICKER, ContentType.VIDEO_NOTE, ContentType.VOICE,
    ContentType.VIDEO, ContentType.DOCUMENT, ContentType.ANIMATION
])
async def take_file(msg: types.Message):
    await msg.reply(Extractor(msg).build_link)


@dp.message_handler(content_types=ContentType.ANY)
async def take_photo(msg: types.Message):
    await msg.reply("This may be a bug, but I don't know how to process your message.")
