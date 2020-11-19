import fileinput
import os
import re
from pathlib import Path


def keep_line(line, data):
    # Skip sub notifications and bots' messages
    for pattern in data['skip_patterns']:
        if re.match(pattern, line):
            return False

    msg_match = re.match(data['message_re'], line)
    if msg_match:
        msg = msg_match[2]
        # Skip common commands
        if msg in data['commands']:
            return False
        # Skip messages consisting of emotes only
        words = msg.split()
        if all(word in data['emotes'] for word in words):
            return False
    return True


def main():
    date_re = r'\[\d\d:\d\d:\d\d\]'
    data = {
        'message_re': rf'{date_re}\s+([^:]+):\s+(.*)'
    }

    data_dir = os.getenv('PROCESSTWITCHLOG_DIR', '.')
    for filename in ['bots', 'commands', 'emotes']:
        path = Path(data_dir, filename)
        try:
            with open(path) as f:
                data[filename] = list(map(lambda s: s.strip(), f))
        except FileNotFoundError:
            data[filename] = []

    notifications = [
        r'is gifting \d+ Tier',
        r'gifted a Tier \d+ sub to',
        'is continuing the Gift Sub',
        'is paying forward the Gift they god',
        'subscribed at Tier',
        'subscribed with Twitch Prime',
        'converted from a Twitch Prime sub'
    ]
    data['skip_patterns'] = list(map(
        lambda notification: rf'{date_re} \S.* {notification}',
        notifications))

    for bot in data['bots']:
        data['skip_patterns'].append(rf'{date_re}  {bot}:')

    for line in fileinput.input():
        if keep_line(line, data):
            print(line, end='')
