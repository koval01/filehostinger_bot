import aiohttp
import config
import logging as log
from aiogram.types import Message


class Extractor:
    def __init__(self, file_id: str, msg: Message = None) -> None:
        self.file_id = file_id
        self.msg = msg

    @property
    async def get_file_data(self) -> dict or None:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        "https://api.telegram.org/bot%s/getFile" % config.BOT_TOKEN,
                        params={"file_id": self.file_id}
                ) as response:
                    return await response.json()["result"]
        except Exception as e:
            log.error("%s: %s" % (self.get_file_data.__name__, e))

    async def check_file_data(self, data: dict) -> str or None:
        try:
            return data["file_path"]
        except Exception as e:
            log.error("%s: %s" % (self.check_file_data.__name__, e))

    def check_size(self, file_data: dict) -> bool:
        return True if 20971520 > file_data["file_size"] else False

    async def build_link(self) -> str or None:
        try:
            resp = await self.get_file_data
            if self.check_size(resp):
                data = await self.check_file_data(resp)
                return "%s/%s" % (config.HOST, data) if data else None
            else:
                await self.msg.reply(
                    "Max size file is 20 megabytes. Read this - https://core.telegram.org/bots/api#file"
                )
        except Exception as e:
            log.error("%s: %s" % (self.build_link.__name__, e))
