import requests_cache
import config
import logging as log
from aiogram.types import Message
from datetime import timedelta

session = requests_cache.CachedSession(
    'cache_extractor', backend='memory', expire_after=timedelta(minutes=30)
)


class Extractor:
    def __init__(self, msg: Message = None, photo: bool = False, file_id: str = None) -> None:
        if msg:
            self.photo = msg.photo[-1:][0] if photo else None
            self.file_id, self.file_size = (self.photo.file_id, self.photo.file_size) if photo else (
                eval("msg.%s.%s" % (msg.content_type, e)) for e in ["file_id", "file_size"]
            )
        else: self.file_id = file_id

    @property
    def get_file_data(self) -> dict or None:
        try:
            response = session.get(
                "https://api.telegram.org/bot%s/getFile" % config.BOT_TOKEN,
                params={"file_id": self.file_id}
            )
            return response.json()["result"]
        except Exception as e:
            log.error("%s: %s" % (self.get_file_data.__name__, e))

    def check_file_data(self, data: dict) -> str or None:
        try:
            return data["file_path"]
        except Exception as e:
            log.error("%s: %s" % (self.check_file_data.__name__, e))

    @property
    def check_size(self) -> bool:
        return True if 20971520 > self.file_size else False

    @property
    def file_data_prepare(self) -> str:
        try:
            resp = self.get_file_data
            data = self.check_file_data(resp)
            return data["file_path"]
        except Exception as e:
            log.error("%s: %s" % (self.file_data_prepare.__name__, e))
        return "Unknown error"

    @property
    def build_link(self) -> str:
        if not self.check_size:
            return "Max size file is 20 megabytes. Read this - https://core.telegram.org/bots/api#file"
        return "%s/%s" % (config.HOST, self.file_id)
