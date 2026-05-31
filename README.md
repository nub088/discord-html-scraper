# Discord Bot-Data Scraper

A lot of Discord bots post useful stuff into a channel over time — price alerts, signals,
status logs, scrape results, whatever. The problem is it's all trapped in chat history mixed
in with everyone else's messages. This pulls one author's messages (say, a bot's) back out of
an exported channel and dumps them to a clean `timestamp :: message` text file you can
actually work with.

It's a small, dependency-free Python script — just the standard library.

## How it works

1. Export the channel to HTML with
   [DiscordChatExporter](https://github.com/Tyrrrz/DiscordChatExporter).
2. Open the HTML and find the user ID of the bot (or whichever author) you want to pull —
   it's in the `data-user-id` attribute on its messages.
3. Drop that ID into `TARGET_ID` in `Scraper.py`, point `html_file` at your export, and run it.

```bash
python Scraper.py
```

It walks the export line by line, tracks the current author and timestamp, keeps only the
messages whose author matches `TARGET_ID`, strips the HTML tags, and writes each one to
`output.txt` as:

```
<timestamp> :: <message text>
```

## Why parse the HTML export instead of hitting the API

Going through DiscordChatExporter's HTML means you don't need a bot token, gateway access,
or to deal with rate limits — you just need read access to the channel and a one-time export.
The trade-off is that the parser keys off DiscordChatExporter's CSS class names
(`chatlog__timestamp`, `chatlog__author`, `chatlog__markdown-preserve`), so if they change
their export format the regexes may need a tweak.

## Notes

- Markdown formatting is stripped — you get plain text, which is usually what you want when
  the messages are structured bot output you're going to parse further.
- One author at a time. Change `TARGET_ID` and re-run to grab a different one.
