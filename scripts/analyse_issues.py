import os
import pandas as pd
import matplotlib.pyplot as plt

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
CHARTS_DIR = os.path.join(os.path.dirname(__file__), "..", "charts")

issues_df = pd.read_csv(os.path.join(DATA_DIR, "issues_clean.csv"))

# Open issues have no resolution time yet, so keep only closed ones
closed = issues_df.dropna(subset=["resolution_hours"]).copy()
closed["resolution_days"] = closed["resolution_hours"] / 24

# Calculate stats on ALL closed issues (before any trimming)
median_days = closed["resolution_days"].median()
mean_days = closed["resolution_days"].mean()
p95 = closed["resolution_days"].quantile(0.95)

print(f"Total issues: {len(issues_df)}")
print(f"Closed issues: {len(closed)}")
print(f"Still open: {len(issues_df) - len(closed)}")
print(f"Median resolution time: {median_days:.1f} days")
print(f"Mean resolution time: {mean_days:.1f} days")
print(f"95th percentile: {p95:.1f} days")

# For the chart only, hide the extreme tail so the shape is visible
trimmed = closed[closed["resolution_days"] <= p95]

fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(trimmed["resolution_days"], bins=30, color="green", edgecolor="white")
ax.axvline(median_days, color="red", linestyle="--",
           label=f"Median: {median_days:.1f} days")
ax.set_title("Issue resolution time - axios/axios (closed issues, top 5% outliers hidden)")
ax.set_xlabel("Days to close")
ax.set_ylabel("Number of issues")
ax.legend()
plt.tight_layout()

chart_path = os.path.join(CHARTS_DIR, "issue_resolution_time.png")
plt.savefig(chart_path, dpi=150)
print(f"Saved chart to {chart_path}")

# Second chart: zoom into the first 60 days
fast = closed[closed["resolution_days"] <= 60]
share_fast = len(fast) / len(closed) * 100
print(f"Closed within 60 days: {len(fast)} issues ({share_fast:.1f}% of closed issues)")

fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.hist(fast["resolution_days"], bins=30, color="green", edgecolor="white")
ax2.axvline(median_days, color="red", linestyle="--",
            label=f"Median (all closed issues): {median_days:.1f} days")
ax2.set_title("Issue resolution time - first 60 days only")
ax2.set_xlabel("Days to close")
ax2.set_ylabel("Number of issues")
ax2.legend()
plt.tight_layout()

zoomed_path = os.path.join(CHARTS_DIR, "issue_resolution_time_zoomed.png")
fig2.savefig(zoomed_path, dpi=150)
print(f"Saved chart to {zoomed_path}")

plt.show()