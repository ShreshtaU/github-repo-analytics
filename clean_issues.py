import json
import pandas as pd

with open("issues_raw.json") as f:
    issues_raw = json.load(f)

BOT_KEYWORDS = ["bot", "dependabot", "[bot]"]

def is_bot(login):
    if not login:
        return False
    return any(keyword in login.lower() for keyword in BOT_KEYWORDS)

issue_rows = []
pr_rows = []

for item in issues_raw:
    is_pr = "pull_request" in item  # True if this is actually a PR, not a real issue

    user = item["user"]
    user_login = user["login"] if user else None  # same None-safety as commits

    row = {
        "number": item["number"],
        "user_login": user_login,
        "is_bot": is_bot(user_login),
        "state": item["state"],
        "created_at": item["created_at"],
        "closed_at": item["closed_at"],  # will be None if still open
    }

    if is_pr:
        pr_rows.append(row)
    else:
        issue_rows.append(row)

# Turn just the true issues into a DataFrame
issues_df = pd.DataFrame(issue_rows)

# Convert both date columns to real datetimes
issues_df["created_at"] = pd.to_datetime(issues_df["created_at"], utc=True)
issues_df["closed_at"] = pd.to_datetime(issues_df["closed_at"], utc=True)

# Calculate how many hours between creation and closing
issues_df["resolution_hours"] = (
    issues_df["closed_at"] - issues_df["created_at"]
).dt.total_seconds() / 3600

issues_df.to_csv("issues_clean.csv", index=False)
print(f"Saved {len(issues_df)} true issues to issues_clean.csv")
print(f"({len(pr_rows)} PRs were filtered out of this file)")
print(issues_df.head())