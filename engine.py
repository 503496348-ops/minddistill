#!/usr/bin/env python3
"""Backward-compatible shim — prefer geo_diag/engine.py."""
from geo_diag.engine import main

if __name__ == "__main__":
    raise SystemExit(main())
