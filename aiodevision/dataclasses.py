import typing
import datetime


class RTFS:
    __slots__ = ('nodes', 'query_time')

    def __init__(self, nodes: str, query_time: float) -> None:
        self.nodes = nodes
        self.query_time = query_time


class RTFM:
    __slots__ = ('nodes', 'query_time')

    def __init__(self, nodes: str, query_time: float) -> None:
        """Base class used for the rtfm function"""
        self.nodes = nodes
        self.query_time = query_time


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

    def __init__(self, data: typing.Dict[str, typing.Union[str, float]]):
        self.upload_count = data['upload_count']
        self.uploaded_today = data['uploaded_today']
        self.last_uploaded = data['last_uploaded']


class UploadStats:
    def __init__(self, data: typing.Dict[str, typing.Union[str, float]]):
        self.url = data['url']
        self.timestamp = datetime.datetime.fromtimestamp(data['timestamp'])
        self.author = data['author']
        self.views = data['views']
        self.node = data['node']
        self.size = data['size']
