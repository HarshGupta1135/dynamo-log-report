"""Verifier for the log-report task.

Exactly one test per numbered success criterion in instruction.md. Ground
truth for the fixed environment/access.log (6 request lines): 6 total
requests, 3 distinct client IPs, and /index.html as the most requested path.
"""

import json
from pathlib import Path

REPORT = Path("/app/report.json")


def test_report_exists():
    """instruction.md criterion 1: a file exists at /app/report.json."""
    assert REPORT.exists(), "no file at /app/report.json"


def test_report_is_json_object():
    """instruction.md criterion 2: the contents are a single valid JSON object."""
    data = json.loads(REPORT.read_text())
    assert isinstance(data, dict), "report.json must be a single JSON object"


def test_total_requests():
    """instruction.md criterion 3: total_requests equals the number of request lines (6)."""
    data = json.loads(REPORT.read_text())
    assert data["total_requests"] == 6


def test_unique_ips():
    """instruction.md criterion 4: unique_ips equals the number of distinct client IPs (3)."""
    data = json.loads(REPORT.read_text())
    assert data["unique_ips"] == 3


def test_top_path():
    """instruction.md criterion 5: top_path is the most frequently requested path (/index.html)."""
    data = json.loads(REPORT.read_text())
    assert data["top_path"] == "/index.html"
