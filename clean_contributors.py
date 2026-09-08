import json
import pandas as pd

with open("contributors_raw.json") as f:
    contributors_raw = json.load(f)

BOT_KEYWORDS = ["bot", "dependabot", "[bot]"]

def is_bot(login):
    if not login:
        return False
    return any(keyword in login.lower() for keyword in BOT_KEYWORDS)

contributors_rows = []

for item in contributors_raw:
    # Named contributors have "login", anonymous ones have "name" instead
    login = item.get("login")
    name = item.get("name")
    is_anonymous = login is None

    row = {
        "user_login": login,
        "anonymous_name": name,       # only filled in for anonymous contributors
        "is_anonymous": is_anonymous,
        "is_bot": is_bot(login),
        "contributions": item["contributions"]
    }

    contributors_rows.append(row)

contributions_df = pd.DataFrame(contributors_rows)
contributions_df = contributions_df.sort_values("contributions", ascending=False)

contributions_df.to_csv("contributions_clean.csv", index=False)
print(f"Saved {len(contributions_df)} contributors to contributions_clean.csv")
print(f"({contributions_df['is_anonymous'].sum()} were anonymous)")
print(contributions_df.head())