# CVPR 2026 GitHub Open Source Audit

Canonical data for tracking GitHub repository availability and star counts for papers listed on the CVPR 2026 paper index.

Data source:

- `results_live.json`: complete JSON array of paper records, including paper metadata, confirmed GitHub repositories, evidence, status, confidence labels, and review notes.

Only the README and canonical JSON data source are pushed to GitHub. The local dashboard, progress file, CSV export, and helper scripts are generated or maintained locally.

Confidence labels distinguish direct/high-confidence matches, reviewed multi-repository official artifacts, candidates that need review, and papers still needing title search.
