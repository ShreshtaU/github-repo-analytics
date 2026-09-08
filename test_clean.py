import json
with open("contributors_raw.json") as f:
    contributors_raw = json.load(f)

for item in contributors_raw:
    print(item.keys())