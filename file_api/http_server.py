from flask import Flask, request, stream_with_context, Response
from werkzeug.routing import BaseConverter
from requests import get as http_get
import config


class RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        self.map = map
        self.regex = args[0]


app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter


@app.route('/<path:type_file>/<regex(".*"):file_name>', methods=['GET'])
def get_file(type_file: str, file_name: str):
    response = http_get(
        'https://api.telegram.org/file/bot%s/%s/%s' % (
            config.BOT_TOKEN, type_file, file_name
        ), stream=True,
        headers={
            'user-agent': request.headers.get('user-agent')
        }
    )
    return Response(
        stream_with_context(response.raw),
        content_type=response.headers.get('content-type'),
        status=response.status_code
    )
