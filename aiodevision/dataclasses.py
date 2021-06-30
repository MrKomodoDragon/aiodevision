import typing
import datetime


class RTFS:
    __slots__ = ('nodes', 'query_time',)

    def __init__(self, data: typing.Dict[str, typing.Any]) -> None:
        print(data)
        self.nodes: typing.Dict[str, typing.Any] = data['nodes']
        self.query_time: float = float(data['query_time'])
        


class RTFM:
    __slots__ = ('nodes', 'query_time', 'cache_indexed', 'cache_expires')

    def __init__(self, data: typing.Dict[str, typing.Any]) -> None:
        """Base class used for the rtfm function"""
        self.nodes: typing.Dict[str, str] = data['nodes']
        self.query_time: float = float(data['query_time'])
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

    def __init__(self, data: typing.Dict[str,typing.Any], query_time: float):
        """Base class that is returned when using the `xkcd` method of Client"""
        self.num: int = int(data['num'])
        self.safe_title: str = data['safe_title']
        self.title: str = data['title']
        self.posted: datetime.datetime = datetime.datetime.fromisoformat(data['posted'])
        self.alt: str = data['alt']
        self.transcript: typing.Optional[str] = data.get('transcript')
        self.news: typing.Optional[str] = data.get('news')
        self.image_url: str = data['image_url']
        self.url: str = data['url']
        self.query_time: float = query_time


class CDN:
    __slots__ = ('url', 'slug', 'node')

    def __init__(self, data: typing.Dict[str, str]):
        self.url: str = data['url']
        self.slug: str = data['slug']
        self.node: str = data['node']


class CDNStats:
    __slots__ = ('upload_count', 'uploaded_today', 'last_uploaded')

    def __init__(self, data: typing.Dict[str, typing.Any]):
        self.upload_count: str = data['upload_count']
        self.uploaded_today: int = int(data['uploaded_today'])
        self.last_uploaded: int = int(data['last_uploaded'])


class UploadStats:
    def __init__(self, data: typing.Dict[str, typing.Any]):
        self.url: str = data['url']
        self.timestamp: datetime.datetime = datetime.datetime.fromtimestamp(data['timestamp'])
        self.author: str = data['author']
        self.view: int = int(data['views'])
        self.node: str = data['node']
        self.size: int = int(data['size'])
