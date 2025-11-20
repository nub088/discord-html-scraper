import re

#1 Input HTML and output text file
html_file   = "discordchatexport.html"   # <-- make sure this is the HTML, NOT output.txt
output_file = "output.txt"

#2 User ID (unique id for precision)
TARGET_ID = "718992882182258769"

#Regex helpers (cleanup)
ts_re   = re.compile(r'title="([^"]+)"')       # for timestamps
uid_re  = re.compile(r'data-user-id=([0-9]+)') # for user IDs
tag_re  = re.compile(r'<[^>]+>')               # strip HTML tags

current_user = None
current_ts   = None
messages     = []

with open(html_file, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        #timestamp
        if "chatlog__timestamp" in line:
            m = ts_re.search(line)
            if m:
                current_ts = m.group(1)

        #author
        if "chatlog__author" in line and "data-user-id" in line:
            m = uid_re.search(line)
            if m:
                current_user = m.group(1)

        #message
        if "chatlog__markdown-preserve" in line and current_user == TARGET_ID:
            #Remove all tags, keep only text
            clean = tag_re.sub("", line).strip()
            if clean:
                messages.append((current_ts, clean))

#)Export to output.txt
with open(output_file, "w", encoding="utf-8") as out:
    for ts, msg in messages:
        out.write(f"{ts} :: {msg}\n")

print(f"Done. Extracted {len(messages)} messages.")
print(f"Saved to: {output_file}")
