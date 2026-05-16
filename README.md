# CVPR 2026 GitHub Open Source Audit

Canonical data for tracking GitHub repository availability and star counts for papers listed on the CVPR 2026 paper index.

Dashboard:

https://puzune.github.io/cvpr2026-github-audit/

Data source:

- `results_live.json`: complete JSON array of paper records, including paper metadata, confirmed GitHub repositories, evidence, status, confidence labels, and review notes.

Visualization:

- `index.html`: public entrypoint.
- `dashboard.html`: static GitHub Pages viewer that reads `results_live.json`.

Only the canonical JSON data source is updated by the recurring sync. The progress file, CSV export, and helper scripts are generated or maintained locally.

Confidence labels distinguish direct/high-confidence matches, reviewed multi-repository official artifacts, candidates that need review, and papers still needing title search.
