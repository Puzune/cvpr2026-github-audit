#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

INTERVAL_SECONDS="${SYNC_INTERVAL_SECONDS:-300}"
FILES=(
  .gitignore
  .nojekyll
  README.md
  index.html
  dashboard.html
  results_live.json
  progress.json
  cvpr2026_papers_github_status_live.csv
  cvpr2026_papers_github_status_live.jsonl
  sync_public_repo.sh
)

sync_once() {
  git add "${FILES[@]}"
  if ! git diff --cached --quiet; then
    git commit -m "Update live audit data $(date '+%Y-%m-%d %H:%M:%S %z')"
    git push origin main
  fi
}

while true; do
  sync_once
  if ! pgrep -f "continue_deep_search.py" >/dev/null; then
    sleep 10
    sync_once
    exit 0
  fi
  sleep "$INTERVAL_SECONDS"
done
