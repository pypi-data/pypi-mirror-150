# py-reddit

A package that can be used to get reddit submissions, and their various attributes.
The package supports both synchronous and asynchronous development.
I am more familiar with synchronous programming, but have tried my best at making a good asynchronous implementation.
The package is written in Python 3.10, and uses requests and aiohttp as its main dependencies.

Updates will be coming soon, thank you for viewing this package, please consider using it.

Version - 1.1.12

Docs - [docs](https://py-reddit.readthedocs.io/en/latest/)

Socials - [KING7077 - GitHub](https://github.com/KING7077)

Installation methods:

```
pip3 install py-reddit

py -3 -m pip install py-reddit

python3 -m pip install py-reddit
```

Example usage:

```py
import reddit

client = reddit.Client('agent', 'key')

subreddit = client.Subreddit('top', 'subreddit-here') # supports 'top', 'new' or 'hot' mode of submissions

print(subreddit.selftext(0)) #gets the selftext of the first post here
```

Asynchronus client:

```py
import reddit
import asyncio

client = reddit.AsyncClient('agent', 'key')


async def main():
    subreddit = await client.Subreddit('top', 'subreddit-here') # supports 'top', 'new' or 'hot' mode of submissions
    print(await subreddit.selftext(0))

asyncio.run(main())
```

The package is still under active development
