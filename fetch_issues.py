import requests
import json
import os

from dotenv import load_dotenv
load_dotenv()

token = os. environ.get("GITHUB_TOKEN")
headers = {"Authorization": f"Bearer {token}"}

all_issues = []
page = 1

while True:
    response = requests.get("https://api.github.com/repos/axios/axios/issues",headers = headers, params = {"per_page": 100, "page": page, "state": "all"})
    if response.status_code != 200:
        print(f"Error {response.status_code} : {response.json()}")
        break

    data = response.json()
    all_issues.extend(data)
    print(f"Page {page}: got {len(data)} issues, total so far: {len(all_issues)}")
    if len(data) <100:
        break
    else:
        page += 1

with open("issues_raw.json", "w") as f:
    json.dump(all_issues, f)

print(f"Saved {len(all_issues)} issues (and PRs mixed in) to issues_raw.json")