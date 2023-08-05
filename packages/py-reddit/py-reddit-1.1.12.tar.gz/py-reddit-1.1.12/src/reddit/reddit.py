import requests
import string
import random
import aiohttp
import inspect


class _AsyncMeta(type):
    async def __call__(self, *args, **kwargs):
        obb = object.__new__(self)
        fn = obb.__init__(*args, **kwargs)
        if inspect.isawaitable(fn):
           await fn
        return obb

class Client:
    """
    Represents a synchronous Client for fetching reddit posts.
    """

    def __init__(self, agent, key):
        self.agent = agent
        self.key = key

    class Subreddit:
        r"""
        Gets the raw data on a subreddit, which can be fetched via the various methods here.

        Parameters
        ----------
        name : `str`
            The name of the subreddit
        mode : `str`
            'top', 'hot', or 'new' kind of posts
        limit : `int`
            The number of posts to fetch, defaults to 25 if not specified
        """

        def __init__(self, mode, name, limit: int = 25):
            self.name = name
            self.mode = mode
            self.limit = limit
            self.agent = ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=8))
            if limit:
                if mode == 'top':
                    self.json = requests.get(
                        'https://www.reddit.com/r/{}/top/.json?limit={}'.format(name, self.limit),
                        headers={'User-Agent': self.agent}).json()
                elif mode == 'hot':
                    self.json = requests.get(
                        'https://www.reddit.com/r/{}/hot/.json?limit={}'.format(name, self.limit),
                        headers={'User-Agent': self.agent}).json()
                elif mode == 'new':
                    self.json = requests.get(
                        'https://www.reddit.com/r/{}/new/.json{}'.format(name, self.limit),
                        headers={'User-Agent': self.agent}).json()

        def selftext(self, index: int):
            r"""
            Returns
            -------
            selftext: `str`
                The selftext of a post at the specified index.
            """
            selftext = self.json['data']['children'][index]['data']['selftext']
            return selftext

        def title(self, index: int):
            r"""
            Returns
            -------
            title: `str`
                The title of a post at the specified index.
            """
            title = self.json['data']['children'][index]['data']['title']
            return title

        def post_url(self, index: int):
            r"""
            Returns
            -------
            post_url: `str`
                The url of a post at the specified index.
            """
            post_url = 'https://reddit.com' + self.json['data']['children'][index]['data']['permalink']
            return post_url

        def author(self, index: int):
            r"""
            Returns
            -------
            author: `str`
                The author of a post at the specified index.
            """
            author = self.json['data']['children'][index]['data']['author']
            return author

        def image(self, index: int):
            r"""
            Returns
            -------
            image: `str`
                The image url in a post at the specified index.

            Raises
            ------
            KeyError
                Raised if there's no image in the post.
            """
            try:
                image = self.json['data']['children'][index]['data']['url_overridden_by_dest']
                return image
            except KeyError:
                raise KeyError('No image found')

        def num_comments(self, index: int):
            r"""
            Returns
            -------
            num_comments: `str`
                The number of comments of a post at the specified index.
            """
            num_comments = self.json['data']['children'][index]['data']['num_comments']
            return num_comments

        def upvotes(self, index: int):
            r"""
            Returns
            -------
            upvotes: `str`
                The number of upvotes in a post at the specified index.
            """
            upvotes = self.json['data']['children'][index]['data']['ups']
            return upvotes

        def downvotes(self, index: int):
            r"""
            Returns
            -------
            downvotes: `str`
                The number of downvotes in a post at the specified index.
            """
            downvotes = self.json['data']['children'][index]['data']['downs']
            return downvotes

        def score(self, index: int):
            r"""
            Returns
            -------
            score: `str`
                The score (upvotes-downvotes) of a post at the specified index.
            """
            score = self.json['data']['children'][index]['data']['score']
            return score

        def permalink(self, index: int):
            r"""
            Returns
            -------
            permalink: `str`
                The permalink of a post at the specified index.
            """
            permalink = self.json['data']['children'][index]['data']['permalink']
            return permalink

        def raw_json(self):
            r"""
            Returns
            -------
            raw_json: `dict`
                The raw json of the response.
            """
            raw_json = self.json
            return raw_json


class AsyncClient:
    """
    Represents an asynchronous Client for fetching reddit posts.
    """

    def __init__(self, agent, key):
        self.agent = agent
        self.key = key

    class Subreddit(metaclass=_AsyncMeta):
        r"""
        Gets the raw data on a subreddit, which can be fetched via the various methods here.

        Parameters
        ----------
        name : `str`
            The name of the subreddit
        mode : `str`
            'top', 'hot', or 'new' kind of posts
        limit : `int`
            The number of posts to fetch, defaults to 25 if not specified
        """

        @staticmethod
        async def subreddit_main(mode, name, limit):
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://www.reddit.com/r/{name}/{mode}.json?limit={limit}") as resp:
                    return await resp.json()

        async def __init__(self, mode, name, limit: int = 25):
            self.name = name
            self.mode = mode
            self.limit = limit
            self.agent = ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=8))
            self.json = await self.subreddit_main(self.mode, self.name, self.limit)


        async def selftext(self, index: int):
            r"""|coro|

            Returns
            -------
            selftext: `str`
                The selftext of a post at the specified index.
            """
            selftext = self.json['data']['children'][index]['data']['selftext']
            return selftext

        async def title(self, index: int):
            r"""|coro|

            Returns
            -------
            title: `str`
                The title of a post at the specified index.
            """
            title = self.json['data']['children'][index]['data']['title']
            return title

        async def post_url(self, index: int):
            r"""|coro|

            Returns
            -------
            post_url: `str`
                The url of a post at the specified index.
            """
            post_url = 'https://reddit.com' + self.json['data']['children'][index]['data']['permalink']
            return post_url

        async def author(self, index: int):
            r"""|coro|

            Returns
            -------
            author: `str`
                The author of a post at the specified index.
            """
            author = self.json['data']['children'][index]['data']['author']
            return author

        async def image(self, index: int):
            r"""|coro|

            Returns
            -------
            image: `str`
                The image url in a post at the specified index.

            Raises
            -------
            KeyError
                If the post at the specified index does not have an image.
            """

            try:
                image = self.json['data']['children'][index]['data']['url_overridden_by_dest']
                return image
            except KeyError:
                raise KeyError('No image found')

        async def num_comments(self, index: int):
            r"""|coro|

            Returns
            -------
            num_comments: `str`
                The number of comments in a post at the specified index.
            """
            num_comments = self.json['data']['children'][index]['data']['num_comments']
            return num_comments

        async def upvotes(self, index: int):
            r"""|coro|

            Returns
            -------
            upvotes: `str`
                The number of upvotes in a post at the specified index.
            """
            upvotes = self.json['data']['children'][index]['data']['ups']
            return upvotes

        async def downvotes(self, index: int):
            r"""|coro|

            Returns
            -------
            downvotes: `str`
                The number of downvotes in a post at the specified index.
            """
            downvotes = self.json['data']['children'][index]['data']['downs']
            return downvotes

        async def score(self, index: int):
            r"""|coro|

            Returns
            -------
            score: `str`
                The score of a post (upvotes-downvotes) at the specified index.
            """
            score = self.json['data']['children'][index]['data']['score']
            return score

        async def permalink(self, index: int):
            r"""|coro|

            Returns
            -------
            permalink: `str`
                The permalink of a post at the specified index.
            """
            permalink = self.json['data']['children'][index]['data']['permalink']
            return permalink

        async def raw_json(self):
            r"""|coro|

            Returns
            -------
            raw_json: `dict`
                The raw json of the response.
            """
            raw_json = self.json
            return raw_json
