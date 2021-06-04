import typing
import datetime


class RTFS:
    __slots__ = ('nodes', 'query_time',)

    def __init__(self, data: typing.Dict[str, str]) -> None:
        self.nodes = data['nodes']
        self.query_time: float = float(data['query_time'])
        


class RTFM:
    __slots__ = ('nodes', 'query_time', 'cache_indexed', 'cache_expires')

    def __init__(self, data: typing.Dict[str, str]) -> None:
        """Base class used for the rtfm function"""
        self.nodes = data['nodes']
        self.query_time = float(data['query_time'])
        self.cache_indexed: datetime.datetime = datetime.datetime.fromisoformat(
            data['_cache_indexed']
        )
        self.cache_expires: datetime.datetime = datetime.datetime.fromisoformat(
            data['_cache_expires']
        )


class XKCD:
    __slots__ = (
        'num',
        'safe_title',
        'title',
        'posted',
        'alt',
        'news',
        'image_url',
        'url',
        'query_time',
    )

    def __init__(self, data: typing.Dict[str, str], query_time: float):
        """Base class that is returned when using the `xkcd` method of Client"""
        self.num = data['num']
        self.safe_title = data['safe_title']
        self.title = data['title']
        self.posted = datetime.datetime.fromisoformat(data['posted'])
        self.alt = data['alt']
        self.transcript = data.get('transcript')
        self.news = data.get('news')
        self.image_url = data['image_url']
        self.url = data['url']
        self.query_time = query_time


class CDN:
    __slots__ = ('url', 'slug', 'node')

    def __init__(self, data: typing.Dict[str, str]):
        self.url = data['url']
        self.slug = data['slug']
        self.node = data['node']


class CDNStats:
    __slots__ = ('upload_count', 'uploaded_today', 'last_uploaded')

    def __init__(self, data: typing.Dict[str, typing.Any]):
        self.upload_count = data['upload_count']
        self.uploaded_today = data['uploaded_today']
        self.last_uploaded = data['last_uploaded']


class UploadStats:
    def __init__(self, data: typing.Dict[str, typing.Any]):
        self.url = data['url']
        self.timestamp = datetime.datetime.fromtimestamp(data['timestamp'])
        self.author = data['author']
        self.views = data['views']
        self.node = data['node']
        self.size = data['size']
