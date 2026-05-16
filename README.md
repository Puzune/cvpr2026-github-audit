# CVPR 2026 GitHub Open Source Audit

Live dashboard for tracking GitHub repository availability and star counts for papers listed on the CVPR 2026 paper index.

Dashboard:

https://puzune.github.io/cvpr2026-github-audit/

Tracked files:

- `dashboard.html`: static dashboard UI.
- `results_live.json`: live data consumed by the dashboard.
- `progress.json`: current audit progress.
- `cvpr2026_papers_github_status_live.csv`: downloadable CSV export.
- `cvpr2026_papers_github_status_live.jsonl`: downloadable JSONL export.

The data is updated from a local audit process. Confidence labels distinguish direct/high-confidence matches, reviewed multi-repository official artifacts, and papers still needing title search. In the CSV export, list-valued columns are JSON arrays so embedded semicolons remain round-trippable.
