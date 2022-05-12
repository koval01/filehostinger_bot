import requests_cache
import config
import logging as log
from aiogram.types import Message
from datetime import timedelta


class Extractor:
    def __init__(self, file_id: str, msg: Message = None) -> None:
        self.session = requests_cache.CachedSession(
            'cache_extractor', backend='memory', expire_after=timedelta(minutes=30)
        )
        self.file_id = file_id
        self.msg = msg

    @property
    def get_file_data(self) -> dict or None:
        try:
            response = self.session.get(
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

    def check_size(self, file_data: dict) -> bool:
        return True if 20971520 > file_data["file_size"] else False

    @property
    def file_data_prepare(self) -> str:
        try:
            resp = self.get_file_data
            if self.check_size(resp):
                data = self.check_file_data(resp)
                return data["file_path"]
            else:
                self.msg.reply(
                    "Max size file is 20 megabytes. Read this - https://core.telegram.org/bots/api#file"
                )
        except Exception as e:
            log.error("%s: %s" % (self.file_data_prepare.__name__, e))
        return "Unknown error"

    @property
    def build_link(self) -> str:
        return "%s/%s" % (config.HOST, self.file_id)
