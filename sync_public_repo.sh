#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

INTERVAL_SECONDS="${SYNC_INTERVAL_SECONDS:-300}"
PUSH_TIMEOUT_SECONDS="${PUSH_TIMEOUT_SECONDS:-180}"
LOCK_FILE=".audit_outputs.lock"
FILES=(
  .gitignore
  .nojekyll
  README.md
  audit_io.py
  index.html
  dashboard.html
  results_live.json
  progress.json
  cvpr2026_papers_github_status_live.csv
  cvpr2026_papers_github_status_live.jsonl
  sync_public_repo.sh
)

sync_once() {
  {
    flock -x 9
    python3 audit_io.py validate-public-snapshot || return 1

    local current_branch
    current_branch="$(git branch --show-current)"
    if [[ "$current_branch" != "main" ]]; then
      echo "refusing to sync from branch '$current_branch'; expected 'main'" >&2
      return 1
    fi

    git add "${FILES[@]}" || return 1
    if ! git diff --cached --quiet; then
      git commit -m "Update live audit data $(date '+%Y-%m-%d %H:%M:%S %z')" || return 1
    fi

    local upstream ahead
    upstream="$(git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null || true)"
    if [[ -n "$upstream" ]]; then
      ahead="$(git rev-list --count "$upstream"..HEAD 2>/dev/null || printf '1')"
    else
      ahead=1
    fi

    if [[ "$ahead" != "0" ]]; then
      timeout "$PUSH_TIMEOUT_SECONDS" git push origin HEAD:main || return 1
    fi
  } 9>"$LOCK_FILE"
}

while true; do
  if ! sync_once; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S %z')] sync failed; will retry" >&2
  fi
  if ! pgrep -f "continue_deep_search.py" >/dev/null; then
    sleep 10
    if ! sync_once; then
      echo "[$(date '+%Y-%m-%d %H:%M:%S %z')] final sync failed" >&2
    fi
    exit 0
  fi
  sleep "$INTERVAL_SECONDS"
done
