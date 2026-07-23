#!/usr/bin/env python3
"""Unified CLI for minddistill. Delegates to geo_diag.engine."""
import sys
import os

# Ensure project root is on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from geo_diag.engine import main  # noqa: E402

if __name__ == '__main__':
    main()
