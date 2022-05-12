import logging

from flask import Flask, request, stream_with_context, Response
from werkzeug.routing import BaseConverter
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
logging.basicConfig(level=logging.INFO)


class Mime:
    def __init__(self, path_or_file: str) -> None:
        mimetypes.init()
        self.path_or_file = path_or_file
        self.mimetypes = mimetypes
        self.pattern = re.compile(r"\.[A-z]*$")

    @property
    def extract(self) -> str:
        return self.mimetypes.types_map[
            re.search(self.pattern, self.path_or_file).group(0)
        ]

    def __str__(self) -> str:
        return self.extract


@app.route('/<path:type_file>/<regex(".*"):file_name>', methods=['GET'])
def get_file(type_file: str, file_name: str):
    media = http_get(
        'https://api.telegram.org/file/bot%s/%s/%s' % (
            config.BOT_TOKEN, type_file, file_name
        ), stream=True,
        headers={
            'user-agent': request.headers.get('user-agent')
        }
    )
    try:
        content_type = Mime(file_name)
    except Exception as e:
        logging.debug("MIME detect error! Details: %s" % e)
        content_type = media.headers.get('Content-Type')
    response = Response(
        stream_with_context(media.raw),
        content_type=content_type,
        status=media.status_code
    )
    response.headers["Content-Disposition"] = "inline"
    return response
