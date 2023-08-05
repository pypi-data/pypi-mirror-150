# CHANGELOG

## May 9, 2022

Added documentation, and added raw_json method for Client.Subreddit and AsyncClient.Subreddit - 1.1.12

## March 28, 2022

Small changes to the project functionality. - 1.1.11

## March 28, 2022

Small changes to the README. - 1.1.10

## March 28, 2022

You no longer need to use `__call__` (Found a way to use async `__init__`) - 1.1.9

## March 16, 2022

Changes to the async client usage (Need to use `__call__()`) - 1.1.8

## March 16, 2022

License changes - 1.1.7

## February 21, 2022

Just changing package DIRs - 1.1.6

## February 21, 2022

Just changing package DIRs - 1.1.5

## February 21, 2022

You can now specify the number of posts you want to fetch in Client.Subreddit() and AsyncClient.Subreddit().
For example:

```py
import reddit

subreddit = reddit.Client('agent', 'key').Subreddit('top', 'memes', 100) # To fetch 100 posts. If a limit is not specified, it defaults to 25
```

Similar for the Async Client

limit does not follow a zero index, but all the methods under Subreddit() follow zero index. This may be changed sooner or later

​- 1.1.4

## February 20, 2022

Bettered the asynchronous implementation of the project. Much faster now. Renamed Client.Subreddit.url to Client.Subreddit.post_url, the same change for the asynchronous client - 1.1.3

## February 19, 2022

Minor changes to the description of the project - 1.1.2

## February 19, 2022

Minor changes to the description of the project - 1.1.1

## February 19, 2022

The project actually works now - 1.1.0

## February 18, 2022

Minor changes to make the project more usuable - 1.0.6

## February 18, 2022

Minor changes to make the project more usuable - 1.0.5

## February 18, 2022

Minor changes to make the project more usuable - 1.0.4

## February 18, 2022

Minor changes to make the project more usuable - 1.0.3

## February 18, 2022

Minor changes to the description of the project - 1.0.2

## February 18, 2022

Initial release - 1.0.1
