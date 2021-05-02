import typing
import datetime


class RTFS:
    def __init__(self, nodes: str, query_time: float) -> None:
        self.nodes = nodes
        self.query_time = query_time


class RTFM:
    def __init__(self, nodes: str, query_time: float) -> None:
        """Base class used for the rtfm function"""
        self.nodes = nodes
        self.query_time = query_time


class XKCD:
    def __init__(self, data: typing.Dict[str, str], query_time: float):
        """Base class that is returned when using the `xkcd` method of Client"""
        self.num = data['num']
        self.safe_title = data['safe_title']
        self.title = data['title']
        self.posted = datetime.date.fromisoformat(data['posted'])
        self.alt = data['alt']
        self.transcript = data.get('transcript')
        self.news = data.get('news')
        self.image_url = data['image_url']
        self.url = data['url']
