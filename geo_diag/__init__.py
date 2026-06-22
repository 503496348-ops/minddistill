"""GEO Diagnostic Report Engine — Unified GEO audit + citability + platform check + report generation + fix generation.

"""

from .engine import run_geo_audit, GeoAuditResult, format_report_text
from .citability_scorer import score_passage
from .platform_check import check_platform_readiness, format_platform_report
from .fixer import (
    generate_fixes_from_audit,
    generate_robots_txt,
    generate_llms_txt,
    generate_jsonld_schema,
    generate_meta_tags,
    generate_full_head_snippet,
    GeoFixes,
)

__all__ = [
    "run_geo_audit",
    "GeoAuditResult",
    "format_report_text",
    "score_passage",
    "check_platform_readiness",
    "format_platform_report",
    "generate_fixes_from_audit",
    "generate_robots_txt",
    "generate_llms_txt",
    "generate_jsonld_schema",
    "generate_meta_tags",
    "generate_full_head_snippet",
    "GeoFixes",
]
