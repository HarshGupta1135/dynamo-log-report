"""Verifier for the log-report task.

These checks grade the *real outcome*: they parse the report the agent produced
and compare it against the known-correct summary of the fixed access.log that
ships in the environment image. Merely creating a (non-empty) file is not enough
to pass.

Ground truth derived from environment/access.log (6 request lines):
  * total_requests = 6
  * unique_ips     = 3  (192.168.0.1, 192.168.0.2, 10.0.0.5)
  * top_path       = "/index.html"  (requested 3 times; /about.html 2, /api/login 1)
"""

import json
from pathlib import Path

import pytest

REPORT_PATH = Path("/app/report.json")

EXPECTED_TOTAL_REQUESTS = 6
EXPECTED_UNIQUE_IPS = 3
EXPECTED_TOP_PATH = "/index.html"


@pytest.fixture(scope="module")
def report():
    """Load and sanity-check the report the agent was asked to produce."""
    assert REPORT_PATH.exists(), f"no report found at {REPORT_PATH}"
    assert REPORT_PATH.stat().st_size > 0, "report.json is empty"

    text = REPORT_PATH.read_text()
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        pytest.fail(f"report.json is not valid JSON: {exc}")

    assert isinstance(data, dict), "report.json must contain a single JSON object"
    return data


def test_total_requests(report):
    """total_requests reflects the number of request lines in the log."""
    assert "total_requests" in report, "missing key: total_requests"
    assert report["total_requests"] == EXPECTED_TOTAL_REQUESTS, (
        f"expected total_requests={EXPECTED_TOTAL_REQUESTS}, "
        f"got {report['total_requests']!r}"
    )


def test_unique_ips(report):
    """unique_ips counts the distinct client IP addresses."""
    assert "unique_ips" in report, "missing key: unique_ips"
    assert report["unique_ips"] == EXPECTED_UNIQUE_IPS, (
        f"expected unique_ips={EXPECTED_UNIQUE_IPS}, got {report['unique_ips']!r}"
    )


def test_top_path(report):
    """top_path is the most frequently requested path."""
    assert "top_path" in report, "missing key: top_path"
    assert report["top_path"] == EXPECTED_TOP_PATH, (
        f"expected top_path={EXPECTED_TOP_PATH!r}, got {report['top_path']!r}"
    )
