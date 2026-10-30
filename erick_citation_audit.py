"""Audit numbered citation references locally; not a factual accuracy evaluator."""

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlparse


def audit(payload):
    if not isinstance(payload, dict) or not isinstance(payload.get("answer"), str):
        raise TypeError("Expected an object with a string 'answer'.")
    sources = payload.get("sources")
    if not isinstance(sources, list):
        raise TypeError("Expected a 'sources' array.")
    indexed = {}
    for source in sources:
        if not isinstance(source, dict):
            raise TypeError("Each source must be an object.")
        number, url = source.get("id"), source.get("url")
        if type(number) is not int or number < 1 or number in indexed:
            raise ValueError("Source IDs must be unique positive integers.")
        if not isinstance(url, str):
            raise TypeError("Each source needs a URL string.")
        indexed[number] = url
    references = {int(value) for value in re.findall(r"\[(\d+)\]", payload["answer"])}
    valid_urls = set()
    for number, url in indexed.items():
        try:
            parsed = urlparse(url)
            if (
                parsed.scheme in {"http", "https"}
                and parsed.hostname
                and not re.search(r"\s", url)
            ):
                valid_urls.add(number)
        except ValueError:
            continue
    resolved = references & valid_urls
    return {
        "unique_references": len(references),
        "resolved_references": len(resolved),
        "reference_resolution_rate": round(len(resolved) / len(references), 3)
        if references
        else None,
        "unknown_references": sorted(references - indexed.keys()),
        "invalid_source_urls": sorted(indexed.keys() - valid_urls),
        "unused_sources": sorted(indexed.keys() - references),
        "method": "Numbered [n] references and URL syntax only. Sources are not fetched.",
        "limitation": "A resolved citation does not establish relevance, truth, or answer quality.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    try:
        result = audit(json.loads(args.input.read_text(encoding="utf-8")))
    except (OSError, ValueError, TypeError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
