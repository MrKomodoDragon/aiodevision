import asyncio
import aiohttp


class UndefinedLibraryError(Exception):
    pass


class RTFS:
    def __init__(self, nodes, query_time) -> None:
        self.nodes = nodes
        self.query_time = query_time


class RTFM:
    def __init__(self, nodes, query_time) -> None:
        self.nodes = nodes
        self.query_time = query_time


class Client:
    def __init__(self, token: str = None):
        self.loop = asyncio.get_event_loop()
        headers = {'Authorization': token.strip()} if token else None
        self.session = aiohttp.ClientSession(headers=headers, loop=self.loop)

    async def rtfs(self, query: str, library: str):
        """This Endpoint indexes a python module, and returns links to the source on github for functions and classes closest to the query provided.

        Current Libraries this endpoint can search are: twitchio, wavelink, aiohttp, and discord.py
        """
        if library not in ['twitchio', 'wavelink', 'aiohttp', 'discord.py']:
            raise UndefinedLibraryError(
                'The Library specficued cannot by queried. Please provide a library from the following list: twitchio, wavelink, discord.py, or aiohttp.'
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
    ):
        """This Endpoint indexes a python module, and returns links to the source on github for functions and classes closest to the query provided.

        Current Libraries this endpoint can search are: twitchio, wavelink, aiohttp, and discord.py
        """
        params = {'query': query, 'location': doc_url}
        async with self.session.get(
            'https://idevision.net/api/public/rtfm', params=params
        ) as resp:
            data = await resp.json()
        return RTFM(data['nodes'], data['query_time'])
