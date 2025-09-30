#!/usr/bin/env python3
"""Fetch sample metrics from selected Oura API endpoints."""
from __future__ import annotations

import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = ROOT / ".env"
OUTPUT_DIR = ROOT / "artifacts" / "oura_samples"

ENDPOINTS = {
    "daily_sleep": ["score", "contributors", "day"],
    "daily_activity": ["score", "steps", "total_calories", "active_calories"],
    "daily_stress": ["day_summary", "stress_high", "recovery_high"],
    "daily_resilience": ["level", "contributors", "day"],
}


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip().lstrip("\ufeff")
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def fetch(endpoint: str, token: str, start_date: str, end_date: str) -> dict:
    base_url = f"https://api.ouraring.com/v2/usercollection/{endpoint}"
    query = urllib.parse.urlencode({"start_date": start_date, "end_date": end_date})
    url = f"{base_url}?{query}"
    request = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = response.read().decode("utf-8")
    return json.loads(payload)


def summarize(endpoint: str, payload: dict) -> dict:
    records = payload.get("data", [])
    summary: dict[str, object] = {
        "endpoint": endpoint,
        "records": len(records),
    }
    if not records:
        return summary

    summary_keys = ENDPOINTS[endpoint]
    sample = records[0]
    sample_summary = {}
    for key in summary_keys:
        value = sample.get(key)
        if isinstance(value, dict):
            sample_summary[key] = {k: value[k] for k in list(value.keys())[:3]}
        else:
            sample_summary[key] = value
    date_field = next((field for field in ("day", "timestamp", "summary_date", "date") if field in sample), None)
    if date_field:
        dates = sorted({record.get(date_field) for record in records if record.get(date_field)})
        summary["date_field"] = date_field
        if dates:
            summary["date_range"] = {
                "start": dates[0],
                "end": dates[-1],
            }
    summary["sample_metrics"] = sample_summary
    return summary


def main() -> int:
    load_dotenv(ENV_FILE)
    token = os.getenv("OURA_PAT")
    if not token:
        print("[ERROR] OURA_PAT is not set in environment or .env", file=sys.stderr)
        return 1

    today = dt.date.today()
    start = today - dt.timedelta(days=2)
    start_date = start.isoformat()
    end_date = today.isoformat()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    summaries: list[dict[str, object]] = []
    for endpoint in ENDPOINTS:
        try:
            payload = fetch(endpoint, token, start_date, end_date)
        except urllib.error.HTTPError as exc:
            print(f"[ERROR] {endpoint} request failed: {exc.code} {exc.reason}", file=sys.stderr)
            try:
                body = exc.read().decode("utf-8")
                print(body, file=sys.stderr)
            except Exception:
                pass
            return 1
        except Exception as exc:  # pylint: disable=broad-except
            print(f"[ERROR] {endpoint} request failed: {exc}", file=sys.stderr)
            return 1

        output_path = OUTPUT_DIR / f"{endpoint}_{start_date}_to_{end_date}.json"
        output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

        summary = summarize(endpoint, payload)
        summaries.append(summary)

    report_path = OUTPUT_DIR / f"summary_{start_date}_to_{end_date}.json"
    report_path.write_text(json.dumps(summaries, indent=2, ensure_ascii=False), encoding="utf-8")

    print("=== Oura API Sample Summary ===")
    print(json.dumps(summaries, indent=2, ensure_ascii=False))
    print(f"詳細なレスポンスは {OUTPUT_DIR} 配下の JSON ファイルで確認できます。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
