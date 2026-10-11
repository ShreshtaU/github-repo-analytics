import os
import pandas as pd
import matplotlib.pyplot as plt

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
CHARTS_DIR = os.path.join(os.path.dirname(__file__), "..", "charts")

# Use whichever spelling your file actually has in the data folder
contributors_df = pd.read_csv(os.path.join(DATA_DIR, "contributors_clean.csv"))

# Humans only, biggest contributor first
humans = contributors_df[contributors_df["is_bot"] == False].copy()
humans = humans.sort_values("contributions", ascending=False).reset_index(drop=True)

# Each person's share of all human commits, as a percentage
total_commits = humans["contributions"].sum()
humans["share_pct"] = humans["contributions"] / total_commits * 100

# Running total of those shares: row 0 = top person, row 1 = top two combined, ...
humans["cumulative_pct"] = humans["share_pct"].cumsum()

# Rank column (1 = top contributor) for the x-axis
humans["rank"] = humans.index + 1

print(f"Human contributors: {len(humans)}")
print(f"Total human commits counted: {total_commits}")
print()
for n in [1, 4, 5, 10]:
    print(f"Top {n:>2} contributors account for {humans.loc[n - 1, 'cumulative_pct']:.1f}% of commits")

# The "bus factor": how many people it takes to reach 50% / 80% of all commits
people_for_50 = humans[humans["cumulative_pct"] >= 50]["rank"].iloc[0]
people_for_80 = humans[humans["cumulative_pct"] >= 80]["rank"].iloc[0]
print()
print(f"People needed to reach 50% of commits: {people_for_50}")
print(f"People needed to reach 80% of commits: {people_for_80}")

# Chart: cumulative share for the top 50 contributors
top_n = 50
subset = humans.head(top_n)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(subset["rank"], subset["cumulative_pct"], color="green", marker="o", markersize=3)
ax.axhline(50, color="gray", linestyle="--", linewidth=1)
ax.axhline(80, color="gray", linestyle="--", linewidth=1)
ax.text(top_n, 51, "50%", ha="right", va="bottom", color="gray")
ax.text(top_n, 81, "80%", ha="right", va="bottom", color="gray")
ax.set_title(f"Contribution concentration - axios/axios (top {top_n} of {len(humans)} human contributors)")
ax.set_xlabel("Contributor rank (1 = most commits)")
ax.set_ylabel("Cumulative % of all human commits")
ax.set_ylim(0, 100)
plt.tight_layout()

chart_path = os.path.join(CHARTS_DIR, "contribution_concentration.png")
plt.savefig(chart_path, dpi=150)
print(f"Saved chart to {chart_path}")
plt.show()