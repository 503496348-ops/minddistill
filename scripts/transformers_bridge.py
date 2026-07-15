#!/usr/bin/env python3
"""Bridge entry for HuggingFace Transformers-style workflows.

This module provides a lightweight, offline-compatible integration point used by
minddistill to represent `huggingface/transformers` mapping status. It does not
perform network/model download in doctor mode.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in os.sys.path:
    os.sys.path.insert(0, str(ROOT))


@dataclass
class BridgeResult:
    ok: bool
    repo: str
    mode: str
    text_checksum: str
    char_count: int
    approx_token_count: int
    extra: dict[str, Any]

    def to_payload(self) -> dict[str, Any]:
        return {
            "status": "ok" if self.ok else "degraded",
            "repo": self.repo,
            "mode": self.mode,
            "result": {
                "text_checksum": self.text_checksum,
                "char_count": self.char_count,
                "approx_token_count": self.approx_token_count,
                "extra": self.extra,
            },
        }


def _sample_text() -> str:
    return "How can I improve this page's SEO readiness for AI models?"


def _get_text(args: argparse.Namespace) -> str:
    if args.text:
        return args.text
    if args.input:
        return Path(args.input).read_text(encoding="utf-8")
    return _sample_text()


def _import_transformers() -> tuple[bool, str | None]:
    try:
        import transformers  # type: ignore

        return True, getattr(transformers, "__version__", None)
    except Exception as exc:  # pragma: no cover - environment-dependent
        return False, str(exc)


def run_once(mode: str, text: str) -> BridgeResult:
    text = (text or "").strip()
    has_transformers, transformers_version = _import_transformers()
    chars = len(text)
    approx_tokens = len(text.split())
    checksum = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
    extra = {
        "transformers_imported": has_transformers,
        "transformers_version": transformers_version,
        "mode": mode,
    }
    return BridgeResult(
        ok=True,
        repo="huggingface/transformers",
        mode=mode,
        text_checksum=checksum,
        char_count=chars,
        approx_token_count=approx_tokens,
        extra=extra,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Minddistill transformers bridge")
    parser.add_argument("--text", help="Input text")
    parser.add_argument("--input", type=Path, help="Input text file")
    parser.add_argument("--compact", action="store_true", help="Output compact JSON")
    parser.add_argument(
        "--mode",
        default="inspect",
        choices=["inspect", "token_count"],
        help="Bridge mode",
    )
    parser.add_argument("--sample", action="store_true", help="Use built-in sample text")
    args = parser.parse_args()

    text = _get_text(args)
    if not text and not args.sample:
        parser.error("no input text provided and --sample not set")

    result = run_once(args.mode, text)
    payload = result.to_payload()
    # keep script output parser-friendly for doctor/API
    print(json.dumps(payload, ensure_ascii=False, indent=None if args.compact else 2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
