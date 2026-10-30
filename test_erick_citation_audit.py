import json
from pathlib import Path

import pytest
from erick_citation_audit import audit


def test_sample_missing_and_unused_references():
    report = audit(
        json.loads(
            Path(__file__).with_name("erick_sample.json").read_text(encoding="utf-8")
        )
    )
    assert report["unknown_references"] == [9]
    assert report["unused_sources"] == [3]
    assert report["reference_resolution_rate"] == 0.667


def test_no_citations_and_invalid_sources():
    assert (
        audit({"answer": "Sin citas", "sources": []})["reference_resolution_rate"]
        is None
    )
    report = audit(
        {
            "answer": "Texto [1] [1] [0]",
            "sources": [{"id": 1, "url": "javascript:alert(1)"}],
        }
    )
    assert report["unique_references"] == 2
    assert report["unknown_references"] == [0]
    assert report["invalid_source_urls"] == [1]
    with pytest.raises(ValueError):
        audit(
            {"answer": "test", "sources": [{"id": 1, "url": "https://example.org"}] * 2}
        )
    with pytest.raises(ValueError):
        audit(
            {"answer": "test", "sources": [{"id": True, "url": "https://example.org"}]}
        )
