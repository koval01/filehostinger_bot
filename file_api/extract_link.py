import aiohttp
import config
import logging as log


class Extractor:
    def __init__(self, file_id: str) -> None:
        self.file_id = file_id

    @property
    async def get_file_data(self) -> dict or None:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        "https://api.telegram.org/bot%s/getFile" % config.BOT_TOKEN,
                        params={"file_id": self.file_id}
                ) as response:
                    return await response.json()
        except Exception as e:
            log.error("%s: %s" % (self.get_file_data.__name__, e))

    async def check_file_data(self, data: dict) -> str or None:
        try:
            return data["result"]["file_path"]
        except Exception as e:
            log.error("%s: %s" % (self.check_file_data.__name__, e))

    async def build_link(self) -> str or None:
        try:
            resp = await self.get_file_data
            data = await self.check_file_data(resp)
            return "%s/%s" % (config.HOST, data) if data else None
        except Exception as e:
            log.error("%s: %s" % (self.build_link.__name__, e))
