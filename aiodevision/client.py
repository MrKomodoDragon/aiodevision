import asyncio
import aiohttp
from io import BytesIO
import imghdr
from .dataclasses import CDN, CDNStats, RTFS, RTFM, UploadStats, XKCD
import typing


class UndefinedLibraryError(Exception):
    pass


class TokenRequired(Exception):
    pass


class InvalidImage(Exception):
    pass


class Client:
    def __init__(self, token: typing.Optional[str]):
        self.loop = asyncio.get_event_loop()
        headers = {'Authorization': token.strip()} if token else None
        self.session = aiohttp.ClientSession(headers=headers, loop=self.loop)
        self.token = token.strip() if token else None

    async def rtfs(
        self, query: typing.Optional[str], library: str, format: typing.Optional[str] = 'links'
    ) -> RTFS:
        if library.lower() not in [
            'twitchio',
            'wavelink',
            'aiohttp',
            'discord.py',
            'discord.py-2'
        ]:
            raise UndefinedLibraryError(
                'The Library specficied cannot by queried. Please provide a library from the following list: twitchio, wavelink, discord.py, or aiohttp.'
            )
        params = {'library': library, 'format': format}
        if query:
            params['query'] = query
        async with self.session.get(
            'https://idevision.net/api/public/rtfs', params=params
        ) as resp:
            data = await resp.json()
        return RTFS(data['nodes'], data['query_time'])

    async def rtfm(
        self,
        query: typing.Optional[str],
        doc_url: str,
    ) -> RTFM:
        params = {'query': query, 'location': doc_url}
        async with self.session.get(
            'https://idevision.net/api/public/rtfm', params=params
        ) as resp:
            data = await resp.json()
        return RTFM(data['nodes'], float(data['query_time']))

    async def ocr(self, image: BytesIO) -> str:
        if not self.token:
            raise TokenRequired('A Token is required to access this endpoint')
        filetype = imghdr.what(image.read(), h=image.read())
        if filetype is None:
            raise InvalidImage(
                'The Image you provided is invalid. Please provide a valid image'
            )
        params: typing.Dict[str, typing.Union[str]] = {'filetype': filetype}
        async with self.session.get(
            'https://idevision.net/api/public/ocr',
            params=params,
            data=image,
        ) as resp:
            data = await resp.json()
        return data['data']

    async def xkcd(self, query: str) -> XKCD:
        params = {'query': query}
        async with self.session.get(
            'https://idevision.net/api/public/xkcd', params=params
        ) as resp:
            data = await resp.json()
        return XKCD(data['nodes'], float(data['query_time']))

    async def xkcd_tags(self, word: str, num: int) -> str:
        payload = {'tag': word, 'num': num}
        async with self.session.put(
            'https://idevision.net/api/public/xkcd/tags', data=payload
        ):
            return 'Succesfully added tags to xkcd comic'

    async def hompage(self, payload: typing.Dict[str, str]):
        if not self.token:
            raise TokenRequired('A Token is required to access this endpoint.')
        async with self.session.post(
            'https://idevision.net/api/homepage', data=payload
        ):
            return 'Successfully set up homepage'

    async def cdn_upload(self, image: BytesIO) -> CDN:
        if not self.token:
            raise TokenRequired('A Token is required to access this endpoint')
        ext = imghdr.what(image.read(), h=image.read())
        if ext is None:
            raise InvalidImage(
                'The Image you provided is invalid. Please provide a valid image'
            )
        headers: typing.Dict[str, str] = {
            'File-Name': 'aiodevision.{0}'.format(ext)
        }
        async with self.session.post(
            'https://idevision.net/', data=image, headers=headers
        ) as resp:
            data: typing.Dict[str, str] = await resp.json()
        return CDN(data)

    async def cdn_stats(self) -> CDNStats:
        async with self.session.get('https://idevision.net/api/cdn') as resp:
            data = await resp.json()
        return CDNStats(data)



    async def get_upload_stats(self, node: str, slug: str):
        if not self.token:
            raise TokenRequired('A Token is required to access this endpoint')
        async with self.session.get(
            'https://idevision.net/api{0}/{1}'.format(node, slug)
        ) as resp:
            data = await resp.json()
            return UploadStats(data)
        
    async def delete_cdn(self, node: str, slug: str) -> str:
        if not self.token:
            raise TokenRequired('A Token is required to access this endpoint')
        url = 'https://idevision.net/api/{0}/{1}'.format(node, slug)
        async with self.session.delete(url):
            return 'Succesfully deleted upload'

