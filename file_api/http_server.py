from flask import Flask, request, stream_with_context
from requests import get as http_get
import config

app = Flask(__name__)


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
    return app.response_class(stream_with_context(response.raw))
