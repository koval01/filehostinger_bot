from aiogram import types
from aiogram.types import ContentType
from dispatcher import dp
from file_api.extract_link import Extractor
import config


@dp.message_handler(content_types=ContentType.PHOTO)
async def take_photo(msg: types.Message):
    await msg.reply(await Extractor(msg.photo[-1:][0].file_id, msg).build_link())


@dp.message_handler(content_types=[ContentType.DOCUMENT, ContentType.ANIMATION])
async def take_file(msg: types.Message):
    await msg.reply(await Extractor(msg.document.file_id, msg).build_link())


@dp.message_handler(content_types=ContentType.STICKER)
async def take_file(msg: types.Message):
    await msg.reply(await Extractor(msg.sticker.file_id, msg).build_link())
