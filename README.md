# process-twitch-log

Sanitizes Twitch chatlogs (as obtained from Chatterino) by removing uninteresting messages, such as subscription notifications, bot messages, bot commands and emote-only messages.

## Usage
```process-twitch-log <file> [<file>...]```

Data is read from files called `bots`, `commands` and `emotes`, which contain one item per line (see example files). By default these files are searched for in the current working directory, but you can specify another directory with the `PROCESSTWITCHLOG_DIR` environment variable.
