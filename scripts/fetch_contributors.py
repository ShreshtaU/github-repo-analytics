import requests
import json
import os

from dotenv import load_dotenv
load_dotenv()

token = os. environ.get("GITHUB_TOKEN")
headers = {"Authorization": f"Bearer {token}"}

all_contributors = []
page = 1

while True:
    response = requests.get("https://api.github.com/repos/axios/axios/contributors",headers = headers, params = {"per_page": 100, "page": page, "anon" : "true"})
    if response.status_code != 200:
        print(f"Error {response.status_code} : {response.json()}")
        break

    data = response.json()
    all_contributors.extend(data)
    print(f"Page {page}: got {len(data)} contributors, total so far: {len(all_contributors)}")
    if len(data) <100:
        break
    else:
        page += 1

with open("contributors_raw.json", "w") as f:
    json.dump(all_contributors, f)

print(f"Saved {len(all_contributors)} Contributors to contributors_raw.json")