import asyncio

from common import send_tweet

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    coroutine = send_tweet("en")
    generated: dict = loop.run_until_complete(coroutine)
