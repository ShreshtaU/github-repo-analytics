import json
with open("issues_raw.json") as f:
    data = json.load(f)

prs_mixed_in = sum(1 for item in data if "pull_request" in item)
true_issues = len(data) - prs_mixed_in
print(f"Total items: {len(data)}")
print(f"True issues: {true_issues}")
print(f"PRs mixed in: {prs_mixed_in}")