import csv
import fcntl
import json
import os
import time
from collections import Counter
from contextlib import contextmanager
from pathlib import Path


WORKDIR = Path(__file__).resolve().parent
RESULTS_JSON = WORKDIR / "results_live.json"
PROGRESS_JSON = WORKDIR / "progress.json"
FINAL_CSV = WORKDIR / "cvpr2026_papers_github_status_live.csv"
FINAL_JSONL = WORKDIR / "cvpr2026_papers_github_status_live.jsonl"
LOCK_FILE = WORKDIR / ".audit_outputs.lock"

FIELDS = [
    "paper_id",
    "type",
    "title",
    "authors",
    "affiliations",
    "abstract",
    "arxiv_id",
    "arxiv",
    "cvpr_url",
    "status",
    "confidence",
    "github_repos",
    "stars",
    "repo_sources",
    "evidence",
    "repo_descriptions",
    "repo_pushed_at",
    "repo_is_fork",
    "site_direct_repos",
    "project_urls",
    "hf_repos",
    "pwc_trusted_repos",
    "invalid_candidate_errors",
    "other_site_links",
    "review_notes",
    "search_rounds",
]


def now():
    return time.strftime("%Y-%m-%d %H:%M:%S")


@contextmanager
def output_lock(lock_path=LOCK_FILE):
    lock_path = Path(lock_path)
    with lock_path.open("a", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def _temp_path(path):
    path = Path(path)
    return path.with_name(f".{path.name}.{os.getpid()}.{time.time_ns()}.tmp")


def write_text_atomic(path, content, encoding="utf-8"):
    path = Path(path)
    tmp = _temp_path(path)
    try:
        with tmp.open("w", encoding=encoding) as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink()


def write_bytes_atomic(path, content):
    path = Path(path)
    tmp = _temp_path(path)
    try:
        with tmp.open("wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink()


def write_json_atomic(path, data):
    write_text_atomic(path, json.dumps(data, ensure_ascii=False))


def read_json(path, default=None):
    path = Path(path)
    if not path.exists() or not path.stat().st_size:
        return {} if default is None else default
    return json.loads(path.read_text(encoding="utf-8"))


def public_rows(rows):
    return [{key: value for key, value in row.items() if not key.startswith("_")} for row in rows]


def csv_cell(value):
    if isinstance(value, list):
        return json.dumps(value, ensure_ascii=False)
    if value is None:
        return ""
    return value


def _write_csv(path, rows, fields):
    tmp = _temp_path(path)
    try:
        with tmp.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            for row in rows:
                writer.writerow({key: csv_cell(row.get(key, "")) for key in fields})
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink()


def _write_jsonl(path, rows):
    tmp = _temp_path(path)
    try:
        with tmp.open("w", encoding="utf-8") as handle:
            for row in rows:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink()


def write_public_outputs(rows, csv_path=FINAL_CSV, jsonl_path=FINAL_JSONL, results_path=RESULTS_JSON, fields=FIELDS):
    public = public_rows(rows)
    with output_lock():
        _write_csv(Path(csv_path), public, fields)
        _write_jsonl(Path(jsonl_path), public)
        write_json_atomic(Path(results_path), public)


def write_progress_snapshot(
    rows,
    updates,
    progress_path=PROGRESS_JSON,
    results_path=RESULTS_JSON,
    include_exports=False,
    csv_path=FINAL_CSV,
    jsonl_path=FINAL_JSONL,
    fields=FIELDS,
):
    public = public_rows(rows)
    with output_lock():
        progress = read_json(progress_path, {})
        progress.update(updates)
        write_json_atomic(progress_path, progress)
        write_json_atomic(results_path, public)
        if include_exports:
            _write_csv(Path(csv_path), public, fields)
            _write_jsonl(Path(jsonl_path), public)


def write_progress_only(updates, progress_path=PROGRESS_JSON):
    with output_lock():
        progress = read_json(progress_path, {})
        progress.update(updates)
        write_json_atomic(progress_path, progress)


def status_counts(rows):
    return dict(Counter(row.get("status", "") for row in rows))


def confidence_counts(rows):
    return dict(Counter(row.get("confidence", "") for row in rows))


def validate_public_snapshot(
    csv_path=FINAL_CSV,
    jsonl_path=FINAL_JSONL,
    results_path=RESULTS_JSON,
    progress_path=PROGRESS_JSON,
):
    rows = read_json(results_path, [])
    progress = read_json(progress_path, {})
    jsonl_rows = []
    if Path(jsonl_path).exists():
        jsonl_rows = [json.loads(line) for line in Path(jsonl_path).read_text(encoding="utf-8").splitlines() if line]
    with Path(csv_path).open(newline="", encoding="utf-8") as handle:
        csv_rows = list(csv.DictReader(handle))

    errors = []
    if len(rows) != len(jsonl_rows):
        errors.append(f"results/jsonl row count mismatch: {len(rows)} != {len(jsonl_rows)}")
    if len(rows) != len(csv_rows):
        errors.append(f"results/csv row count mismatch: {len(rows)} != {len(csv_rows)}")
    if progress.get("total_papers") not in {None, len(rows)}:
        errors.append(f"progress total_papers mismatch: {progress.get('total_papers')} != {len(rows)}")
    actual_status = status_counts(rows)
    if progress.get("status_counts") and progress.get("status_counts") != actual_status:
        errors.append(f"progress status_counts mismatch: {progress.get('status_counts')} != {actual_status}")
    jsonl_status = status_counts(jsonl_rows)
    if jsonl_rows and jsonl_status != actual_status:
        errors.append(f"jsonl status_counts mismatch: {jsonl_status} != {actual_status}")
    csv_status = dict(Counter(row.get("status", "") for row in csv_rows))
    if csv_rows and csv_status != actual_status:
        errors.append(f"csv status_counts mismatch: {csv_status} != {actual_status}")

    ids = [str(row.get("paper_id", "")).strip() for row in rows]
    if len(ids) != len(set(ids)):
        errors.append("duplicate paper_id values")
    if any(row.get("status") == "github_found" and not row.get("github_repos") for row in rows):
        errors.append("github_found row without github_repos")
    for row in rows:
        repos = row.get("github_repos") or []
        if len(repos) != len(row.get("stars") or []) or len(repos) != len(row.get("repo_sources") or []):
            errors.append(f"repo metadata length mismatch for paper_id={row.get('paper_id')}")
            break
    return errors


def _main():
    if len(os.sys.argv) > 1 and os.sys.argv[1] == "validate-public-snapshot":
        errors = validate_public_snapshot()
        if errors:
            for error in errors:
                print(error, file=os.sys.stderr)
            raise SystemExit(1)
        print("public snapshot ok")
        return
    raise SystemExit("usage: python3 audit_io.py validate-public-snapshot")


if __name__ == "__main__":
    _main()
