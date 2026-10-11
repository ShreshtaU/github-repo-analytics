import pandas as pd
import matplotlib.pyplot as plt
import os

# Build a path that works regardless of where you run the script from
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
CHARTS_DIR = os.path.join(os.path.dirname(__file__), "..", "charts")

# Load the clean contributors data.
contributors_df = pd.read_csv(os.path.join(DATA_DIR, "contributors_clean.csv"))

# Remove bots - we want to see the humans
humans = contributors_df[contributors_df["is_bot"] == False].copy()

# Anonymous contributors have no login, so fall back to their commit name
# for the chart label (otherwise their label would be blank/NaN)
humans["label"] = humans["user_login"].fillna(humans["anonymous_name"])

# Take the top 15 (CSV is already sorted by contributions, highest first)
top_15 = humans.sort_values("contributions", ascending=False).head(15)

# Build the horizontal bar chart
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(top_15["label"], top_15["contributions"], color="green")
ax.invert_yaxis()  # puts the #1 contributor at the top instead of the bottom
ax.set_title("Top 15 human contributors - axios/axios")
ax.set_xlabel("Number of commits")
plt.tight_layout()

chart_path = os.path.join(CHARTS_DIR, "top_contributors.png")
plt.savefig(chart_path, dpi=150)
print(f"Saved chart to {chart_path}")
plt.show()