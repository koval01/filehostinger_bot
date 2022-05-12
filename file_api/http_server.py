import aiohttp

from aiohttp import web
from aiohttp import streamer


@streamer
async def file_sender(writer, file=None):
    with open(file, 'rb') as f:
        chunk = f.read(2 ** 16)
        while chunk:
            await writer.write(chunk)
            chunk = f.read(2 ** 16)


async def download_file(request):
    headers = {
        "Content-disposition": "inline"
    }
    return web.Response(
        body=file_sender(file_path=await download_file_from_tg()),
        headers=headers
    )


async def download_file_from_tg(url: str) -> bytes:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                return resp.content.read()


app = web.Application()
app.router.add_get('/file/{file_name}', download_file)
