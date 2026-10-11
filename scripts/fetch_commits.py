import requests
import json
import os

from dotenv import load_dotenv
load_dotenv()

token = os. environ.get("GITHUB_TOKEN")
headers = {"Authorization": f"Bearer {token}"}

all_commits = []
page = 1

while True:
    response = requests.get("https://api.github.com/repos/axios/axios/commits",headers = headers, params = {"per_page": 100, "page": page})
    data = response.json()
    all_commits.extend(data)
    print(f"Page {page}: got {len(data)} commits, total so far: {len(all_commits)}")
    if len(data) <100:
        break
    else:
        page += 1

with open("commits_raw.json", "w") as f:
    json.dump(all_commits, f)
print(f"Saved {len(all_commits)} commits to commits_raw.json")