"""GEO Diagnostic Report Engine — Unified GEO audit + citability + platform check + report generation.

"""

from .engine import run_geo_audit, GeoAuditResult, format_report_text
from .citability_scorer import score_passage
from .platform_check import check_platform_readiness, format_platform_report

__all__ = [
    "run_geo_audit",
    "GeoAuditResult",
    "format_report_text",
    "score_passage",
    "check_platform_readiness",
    "format_platform_report",
]
