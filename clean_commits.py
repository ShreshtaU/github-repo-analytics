import json
import pandas as pd

# Load the raw data back in
with open("commits_raw.json") as f:
    commits_raw = json.load(f)

# Bot detection - simple keyword check on the username
BOT_KEYWORDS = ["bot", "dependabot", "[bot]"]

def is_bot(login):
    if not login:
        return False
    return any(keyword in login.lower() for keyword in BOT_KEYWORDS)

# Build a flat list of dictionaries - one clean dict per commit
rows = []
for c in commits_raw:
    commit_info = c["commit"]  # nested dict with author/message/date
    author_login = c["author"]["login"] if c["author"] else None  # can be None!

    rows.append({
        "sha": c["sha"],
        "author_name": commit_info["author"]["name"],
        "author_login": author_login,
        "is_bot": is_bot(author_login),
        "date": commit_info["author"]["date"],
        "message": commit_info["message"].split("\n")[0]  # first line only
    })

# Turn the list of flat dicts into a pandas DataFrame - like a spreadsheet
df = pd.DataFrame(rows)

# Convert the date column from text to real datetime objects
df["date"] = pd.to_datetime(df["date"], utc=True)

# Now that it's a real datetime, we can pull useful parts out of it
df["day_of_week"] = df["date"].dt.day_name()
df["hour"] = df["date"].dt.hour

# Save as CSV - a proper flat table, opens fine in Excel
df.to_csv("commits_clean.csv", index=False)
print(f"Saved {len(df)} cleaned commits to commits_clean.csv")
print(df.head())  # preview the first 5 rows
print(df["is_bot"].value_counts())