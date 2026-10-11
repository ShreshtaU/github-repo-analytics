# GitHub Repository Analytics: axios/axios

A Python data pipeline and Power BI dashboard that extracts the complete
history of the axios open-source repository from the GitHub REST API and
analyzes how the project is maintained: who contributes, how quickly issues
are closed, and how quickly pull requests are merged.



## Key findings

- **Issues:** median time to close is 16.6 days (mean 217.7), across 5,013
  closed issues. The mean is far higher because a minority of issues stay
  open for years, so the median is the representative figure.
- **Pull requests:** 53.8% of 2,776 PRs were merged. Human PRs have a median
  merge time of 3.6 days; bot PRs (e.g. dependabot) merge in about 8 hours.
  Bots are excluded from the human figures.
- **Contribution concentration:** five contributors account for 51.8% of all
  human commits, while reaching 80% takes 264 of 657 contributors.
- **Activity over time:** [add 1-2 sentences from your commits chart,
  e.g. busy early years, quieter 2018-2020, renewed activity from 2021]

## Data

| Source | Records |
|---|---|
| Commits | 2,180 |
| Issues (excluding PRs) | 5,061 |
| Pull requests | 2,776 |
| Contributors | 661 (216 anonymous) |

Data was collected from the GitHub REST API on [date you fetched].

## Method

1. **Fetch:** paginated API calls with token authentication
2. **Clean:** flatten nested JSON, separate issues from PRs, flag bots,
   parse timestamps, compute resolution and merge durations
3. **Analyze:** pandas and matplotlib charts
4. **Dashboard:** Power BI report built on the cleaned CSVs

## Data cleaning decisions

- GitHub's `/issues` endpoint returns pull requests mixed in with issues.
  They are separated using the `pull_request` field.
- Bots are identified by GitHub's `[bot]` account suffix.
- Anonymous contributors (commits with emails not linked to a GitHub
  account) are included via the API's `anon` parameter and labelled by name.
- Medians are reported instead of means because the distributions are
  heavily right-skewed.

## Limitations

- Data is a snapshot; counts differ slightly between endpoints because the
  repository changed while collecting (2,776 PRs vs 2,758 PRs in the issues
  endpoint).
- Contributor counts come from GitHub's cached contributors endpoint and may
  differ from the repository's contributor graph.
- Some people appear under two identities (e.g. a linked username and an
  anonymous name), so concentration figures are approximate.
- Issue resolution time covers closed issues only, and recent years look
  faster partly because only quickly-closed issues from those years can
  appear.
- Resolution time measures time to close, not time spent working on an issue.

## Project structure

    scripts/    fetch, clean and analysis scripts
    data/       raw JSON and cleaned CSVs
    charts/     generated charts
    dashboard/  Power BI file

## How to run

1. Create a virtual environment and run `pip install -r requirements.txt`
2. Create a `.env` file containing `GITHUB_TOKEN=your_token_here`
3. Run the fetch, clean, then analyse scripts in `scripts/`

## Future improvements

- Scheduled incremental updates using the API's `since` parameter
- Merge duplicate contributor identities by commit email
- Attribute issue closures to individual maintainers

## Tech stack

Python, pandas, matplotlib, requests, python-dotenv, Power BI
