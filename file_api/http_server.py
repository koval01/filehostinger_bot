import logging

from flask import Flask, request, stream_with_context, Response, redirect
from flask_caching import Cache
from werkzeug.routing import BaseConverter
from file_api.extract_link import Extractor
from requests import get as http_get
import config
import mimetypes
import re


class RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        self.map = map
        self.regex = args[0]


app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)
logging.basicConfig(level=logging.INFO)


class Mime:
    def __init__(self, path_or_file: str, default_mime: str = "application/octet-stream") -> None:
        mimetypes.init()
        self.path_or_file = path_or_file
        self.mimetypes = mimetypes
        self.default_mime = default_mime
        self.pattern = re.compile(r"\.[A-z0-9]*$")

    @property
    def extract(self) -> str:
        try:
            return self.mimetypes.types_map[
                re.search(self.pattern, str(self.path_or_file)).group(0)
            ]
        except:
            return ""

    @property
    def alter_type(self) -> str:
        try:
            content_type = self.extract
            if not content_type:
                raise
            return content_type
        except Exception as e:
            logging.debug("MIME detect error! Details: %s" % e)
            return self.default_mime

    def __str__(self) -> str:
        return self.alter_type


@app.route('/')
def to_bot() -> redirect:
    return redirect("https://t.me/%s" % config.BOT_NAME, code=301)


@app.route('/<regex(".*"):file_id>', methods=['GET'])
@cache.cached(timeout=600)
def get_file(file_id: str) -> Response:
    data = Extractor(file_id=file_id)
    media = http_get(
        'https://api.telegram.org/file/bot%s/%s' % (
            config.BOT_TOKEN, data
        ), stream=True,
        headers={
            'user-agent': request.headers.get('user-agent')
        }
    )
    response = Response(
        stream_with_context(media.raw),
        content_type=Mime(data),
        status=media.status_code
    )
    response.headers["Content-Disposition"] = "inline"
    return response


if __name__ == "__main__":
    app.run()
