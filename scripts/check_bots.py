import os
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

for filename, name_column in [
    ("pulls_clean.csv", "user_login"),
    ("issues_clean.csv", "user_login"),
    ("commits_clean.csv", "author_login"),
    ("contributors_clean.csv", "user_login"),
]:
    df = pd.read_csv(os.path.join(DATA_DIR, filename))
    flagged = df[df["is_bot"] == True]
    print(f"--- {filename}: {len(flagged)} rows flagged as bot ---")
    print(flagged[name_column].value_counts())
    print()