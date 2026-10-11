import os
import pandas as pd
import matplotlib.pyplot as plt

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
CHARTS_DIR = os.path.join(os.path.dirname(__file__), "..", "charts")

pulls_df = pd.read_csv(os.path.join(DATA_DIR, "pulls_clean.csv"))

# Only merged PRs have a merge time. Closed-without-merging PRs were rejected.
merged = pulls_df[pulls_df["was_merged"] == True].copy()
merged["merge_days"] = merged["merged_hours"] / 24

# Split into bot PRs (e.g. dependabot) and human PRs
bots = merged[merged["is_bot"] == True]
humans = merged[merged["is_bot"] == False]

print(f"Total PRs: {len(pulls_df)}")
print(f"Merged PRs: {len(merged)} ({len(merged) / len(pulls_df) * 100:.1f}% merge rate)")
print(f"  from humans: {len(humans)}")
print(f"  from bots: {len(bots)}")
print()

# Compare the two groups side by side
for name, group in [("ALL", merged), ("HUMANS", humans), ("BOTS", bots)]:
    print(f"{name}: median {group['merge_days'].median():.2f} days, "
          f"mean {group['merge_days'].mean():.1f} days, "
          f"95th percentile {group['merge_days'].quantile(0.95):.1f} days")

# Chart humans only, because the question is "how fast do people get reviewed?"
median_days = humans["merge_days"].median()
p95 = humans["merge_days"].quantile(0.95)
trimmed = humans[humans["merge_days"] <= p95]

fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(trimmed["merge_days"], bins=30, color="green", edgecolor="white")
ax.axvline(median_days, color="red", linestyle="--",
           label=f"Median: {median_days:.1f} days")
ax.set_title("PR merge time - axios/axios (human PRs, top 5% outliers hidden)")
ax.set_xlabel("Days to merge")
ax.set_ylabel("Number of PRs")
ax.legend()
plt.tight_layout()

chart_path = os.path.join(CHARTS_DIR, "pr_merge_time.png")
plt.savefig(chart_path, dpi=150)
print(f"Saved chart to {chart_path}")
plt.show()