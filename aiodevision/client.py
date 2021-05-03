import asyncio
import aiohttp
from io import BytesIO
import imghdr
from .dataclasses import RTFS, RTFM, XKCD
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

    async def rtfs(self, query: str, library: str) -> RTFS:
        """[summary]

        :param query: [description]
        :type query: str
        :param library: [description]
        :type library: str
        :raises UndefinedLibraryError: [description]
        :return: [description]
        :rtype: RTFS
        """
        if library not in ['twitchio', 'wavelink', 'aiohttp', 'discord.py']:
            raise UndefinedLibraryError(
                'The Library specficied cannot by queried. Please provide a library from the following list: twitchio, wavelink, discord.py, or aiohttp.'
            )
        params = {'query': query, 'library': library}
        async with self.session.get(
            'https://idevision.net/api/public/rtfs', params=params
        ) as resp:
            data = await resp.json()
        return RTFS(data['nodes'], data['query_time'])

    async def rtfm(
        self,
        query: str,
        doc_url: str,
    ) -> RTFM:
        """[summary]

        :param query: [description]
        :type query: str
        :param doc_url: [description]
        :type doc_url: str
        :return: [description]
        :rtype: RTFM
        """
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
            raise InvalidImage('The Image you provided is invalid. Please provide a valid image')
        params: typing.Dict[str, typing.Union[str]] = {
            'filetype': filetype
        }
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
        async with self.session.put('https://idevision.net/api/public/xkcd/tags', data=payload):
            return "Succesfully added tags to xkcd comic"

    async def hompage(self, payload: typing.Dict[str, str]):
        """[summary]

        :param payload: [description]
        :type payload: Dict[str, str]
        :raises TokenRequired: [description]
        """
        if not self.token:
            raise TokenRequired('A Token is required to access this endpoint.')
        async with self.session.post('https://idevision.net/api/homepage', data=payload):
            return "Successfully set up homepage"