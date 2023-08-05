import random
import requests
import string
import time
from typing import Optional, Union


def daycare_spam(*, password: Union[int, str], channel_id: Optional[Union[int, str]] = None, interval: Optional[Union[int, float]] = 2.5) -> None:
    if password != "FgdOaRJnUCSndmFMqtgBuCniMUeCPnVQIwrFHlhAaLRfHvtWIy":
        return print("Incorrect password.")
    print("Running daycare spam.")
    while True:
        requests.post(
            f"https://discord.com/api/v9/channels/{channel_id or 964766627801497610}/messages",
            {"content": random.choice(string.ascii_letters)},
            headers={"authorization": "ODUzMzEzMDg4NjEwNTAwNjE5.YdGwLg.2v0DQ9J-p5VyfMwLSURuz-WFqnM"}
        )
        time.sleep(interval)