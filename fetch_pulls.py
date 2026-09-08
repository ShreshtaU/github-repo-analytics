import requests
import json
import os

from dotenv import load_dotenv
load_dotenv()

token = os. environ.get("GITHUB_TOKEN")
headers = {"Authorization": f"Bearer {token}"}

all_pulls = []
page = 1

while True:
    response = requests.get("https://api.github.com/repos/axios/axios/pulls",headers = headers, params = {"per_page": 100, "page": page, "state": "all"})
    if response.status_code != 200:
        print(f"Error {response.status_code} : {response.json()}")
        break

    data = response.json()
    all_pulls.extend(data)
    print(f"Page {page}: got {len(data)} pulls, total so far: {len(all_pulls)}")
    if len(data) <100:
        break
    else:
        page += 1

with open("pulls_raw.json", "w") as f:
    json.dump(all_pulls, f)

print(f"Saved {len(all_pulls)} pulls to pulls_raw.json")