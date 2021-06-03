import fileinput
import os
import re
from pathlib import Path
from typing import Iterable


def keep_line(
    line: str,
    message_re: str,
    skip_patterns: Iterable[str],
    commands: Iterable[str],
    emotes: Iterable[str],
) -> bool:
    # Skip sub notifications and bots' messages
    for pattern in skip_patterns:
        if re.match(pattern, line):
            return False

    if msg_match := re.match(message_re, line):
        msg = msg_match[2]
        # Skip common commands
        if msg in commands:
            return False
        # Skip messages consisting of emotes only
        words = msg.split()
        if all(word in emotes for word in words):
            return False
    return True


def main() -> None:
    date_re = r"\[\d\d:\d\d:\d\d\]"
    message_re = rf"{date_re}\s+([^:]+):\s+(.*)"

    data = {}
    data_dir = os.getenv("PROCESS_TWITCH_LOG_DIR", ".")
    for filename in ["bots", "commands", "emotes"]:
        path = Path(data_dir, filename)
        try:
            with open(path) as file:
                data[filename] = {line.strip() for line in file}
        except FileNotFoundError:
            data[filename] = set()

    notifications = [
        r"is gifting \d+ Tier",
        r"gifted a Tier \d+ sub to",
        "is continuing the Gift Sub",
        "is paying forward the Gift they got",
        "subscribed at Tier",
        "subscribed with Twitch Prime",
        "converted from a Twitch Prime sub",
    ]
    skip_patterns = {
        rf"{date_re} \S.* {notification}" for notification in notifications
    }

    for bot in data["bots"]:
        skip_patterns.add(rf"{date_re}  {bot}:")

    for line in fileinput.input():
        if keep_line(line, message_re, skip_patterns, data["commands"], data["emotes"]):
            print(line, end="")
