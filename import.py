import plistlib
import sys
import io
import bplist
import requests
import json
import os


def send_to_pocket(actions):
    actions_json = json.dumps(actions)
    print(actions_json)
    response = requests.get(
        "https://getpocket.com/v3/send",
        params={
            "actions": actions_json,
            "access_token": os.environ["ACCESS_TOKEN"],
            "consumer_key": os.environ["CONSUMER_KEY"],
        },
    )
    print(response.headers)
    response.raise_for_status()


with open("Bookmarks.plist", "rb") as fh:
    data = plistlib.load(fh)

actions = []
stop_title = os.environ["STOP_TITLE"]
if len(stop_title) == 0:
    stop_title = None

for node in data["Children"]:
    try:
        if node["Title"] == "com.apple.ReadingList":
            for subnode in node["Children"]:
                try:
                    url = subnode["URLString"]
                except KeyError:
                    print("oh no")
                    sys.exit(1)
                try:
                    title = subnode["URIDictionary"]["title"]
                except KeyError:
                    title = None
                d = io.BytesIO(subnode["Sync"]["Data"])
                p = bplist.load(d)
                p2 = bplist.deserialise_NsKeyedArchiver(p, parse_whole_structure=True)
                if "file://" in url:
                    continue
                actions.append({"action": "add", "title": title, "url": url})
                if len(actions) > 10:
                    send_to_pocket(actions)
                    actions = []
                if stop_title and stop_title in title:
                    print("yay")
                    break
    except KeyError:
        pass
if len(actions):
    send_to_pocket(actions)
