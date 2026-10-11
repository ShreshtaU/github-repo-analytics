import pandas as pd
import matplotlib.pyplot as plt
import os

# Build a path that works regardless of where you run the script from
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
CHARTS_DIR = os.path.join(os.path.dirname(__file__), "..", "charts")

# Load the clean commits data, with dates parsed automatically
commits_path = os.path.join(DATA_DIR, "commits_clean.csv")
commits_df = pd.read_csv(commits_path, parse_dates=["date"])

# Filter out bots - we only want human activity for this chart
human_commits = commits_df[commits_df["is_bot"] == False]

# Group by week and count commits per week
weekly_counts = human_commits.groupby(human_commits["date"].dt.to_period("W")).size()
weekly_counts.index = weekly_counts.index.to_timestamp()

# Build the chart
plt.figure(figsize=(10, 5))
plt.plot(weekly_counts.index, weekly_counts.values, color="green")
plt.title("Human commits per week - axios/axios")
plt.xlabel("Week")
plt.ylabel("Number of commits")
plt.xticks(rotation=45)
plt.tight_layout()

# Save into the charts folder, not wherever the script happens to run from
chart_path = os.path.join(CHARTS_DIR, "commits_over_time.png")
plt.savefig(chart_path, dpi=150)
print(f"Saved chart to {chart_path}")

plt.show()