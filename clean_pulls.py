import json
import pandas as pd

with open("pulls_raw.json") as f:
    pulls_raw = json.load(f)

BOT_KEYWORDS = ["bot", "dependabot", "[bot]"]

def is_bot(login):
    if not login:
        return False
    return any(keyword in login.lower() for keyword in BOT_KEYWORDS)

pulls_rows = []

for item in pulls_raw:

    user = item["user"]
    user_login = user["login"] if user else None  # same None-safety as commits
    merged_at = item["merged_at"]
    was_merged = True if merged_at else False

    row = {
        "number": item["number"],
        "user_login": user_login,
        "is_bot": is_bot(user_login),
        "state": item["state"],
        "created_at": item["created_at"],
        "closed_at": item["closed_at"],  # will be None if still open
        "merged_at" : item["merged_at"],
        "was_merged" : was_merged
        
    }
    pulls_rows.append(row)


# Turn just the true issues into a DataFrame
pulls_df = pd.DataFrame(pulls_rows)

# Convert both date columns to real datetimes
pulls_df["created_at"] = pd.to_datetime(pulls_df["created_at"], utc=True)
pulls_df["closed_at"] = pd.to_datetime(pulls_df["closed_at"], utc=True)
pulls_df["merged_at"] = pd.to_datetime(pulls_df["merged_at"], utc=True)

# Calculate how many hours between creation and closing
pulls_df["merged_hours"] = (
    pulls_df["merged_at"] - pulls_df["created_at"]
).dt.total_seconds() / 3600

pulls_df.to_csv("pulls_clean.csv", index=False)
print(f"Saved {len(pulls_df)} true pulls to pulls_clean.csv")
print(pulls_df.head())
print(pulls_df["was_merged"].value_counts())
print(pulls_df["merged_hours"].describe())