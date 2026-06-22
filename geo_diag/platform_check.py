"""Platform-specific AI search readiness checker.

Checks optimization for:
- ChatGPT Search (OAI-SearchBot)
- Perplexity (PerplexityBot)
- Google AI Overviews (Gemini)
- Claude (ClaudeBot)
"""

import re
from dataclasses import dataclass, field
from typing import Optional

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False


@dataclass
class PlatformResult:
    """Result for a single platform check."""
    platform: str
    score: int  # 0-100
    signals: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)


def check_platform_readiness(html: str) -> dict[str, PlatformResult]:
    """Check readiness for all AI platforms.

    Args:
        html: Raw HTML content of the page.

    Returns:
        Dict mapping platform name to PlatformResult.
    """
    if not HAS_BS4:
        return {}

    soup = BeautifulSoup(html, "html.parser")
    results = {}

    # Common signals
    has_schema = soup.find("script", type="application/ld+json") is not None
    has_meta_desc = soup.find("meta", attrs={"name": "description"}) is not None
    has_canonical = soup.find("link", rel="canonical") is not None
    has_og = soup.find("meta", property="og:title") is not None
    h1_tags = soup.find_all("h1")
    h2_tags = soup.find_all("h2")

    # ── ChatGPT Search ──
    chatgpt = PlatformResult(platform="ChatGPT Search", score=0)
    if has_canonical:
        chatgpt.signals.append("Canonical URL present")
        chatgpt.score += 25
    else:
        chatgpt.gaps.append("Missing canonical URL")
    if has_schema:
        chatgpt.signals.append("JSON-LD schema present")
        chatgpt.score += 30
    else:
        chatgpt.gaps.append("Add JSON-LD structured data")
    if has_meta_desc:
        chatgpt.signals.append("Meta description present")
        chatgpt.score += 25
    else:
        chatgpt.gaps.append("Add meta description")
    if has_og:
        chatgpt.signals.append("Open Graph tags present")
        chatgpt.score += 20
    else:
        chatgpt.gaps.append("Add Open Graph meta tags")
    results["ChatGPT Search"] = chatgpt

    # ── Perplexity ──
    perp = PlatformResult(platform="Perplexity", score=0)
    if h1_tags:
        perp.signals.append(f"Found {len(h1_tags)} H1 tag(s)")
        perp.score += 25
    else:
        perp.gaps.append("Add an H1 heading")
    if len(h2_tags) >= 3:
        perp.signals.append(f"Good heading structure ({len(h2_tags)} H2s)")
        perp.score += 25
    else:
        perp.gaps.append("Add more H2 subheadings (3+)")
    if has_meta_desc:
        perp.signals.append("Meta description present")
        perp.score += 20
    else:
        perp.gaps.append("Add meta description")
    if has_schema:
        perp.signals.append("Structured data present")
        perp.score += 30
    else:
        perp.gaps.append("Add JSON-LD schema markup")
    results["Perplexity"] = perp

    # ── Gemini AI Overviews ──
    gemini = PlatformResult(platform="Gemini AI Overviews", score=0)
    if has_schema:
        gemini.signals.append("JSON-LD schema present")
        gemini.score += 35
    else:
        gemini.gaps.append("Add JSON-LD structured data (critical for Gemini)")
    if has_meta_desc:
        gemini.signals.append("Meta description present")
        gemini.score += 25
    else:
        gemini.gaps.append("Add meta description")

    # FAQ schema check
    faq_found = False
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            import json
            data = json.loads(script.string)
            if isinstance(data, dict) and data.get("@type") == "FAQPage":
                faq_found = True
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and item.get("@type") == "FAQPage":
                        faq_found = True
        except (json.JSONDecodeError, TypeError):
            pass

    if faq_found:
        gemini.signals.append("FAQ schema present")
        gemini.score += 40
    else:
        gemini.gaps.append("Add FAQ schema for AI Overview snippets")
    results["Gemini AI Overviews"] = gemini

    # ── Claude ──
    claude = PlatformResult(platform="Claude", score=0)
    if has_meta_desc:
        claude.signals.append("Meta description present")
        claude.score += 25
    else:
        claude.gaps.append("Add meta description")
    if has_schema:
        claude.signals.append("Structured data present")
        claude.score += 25
    else:
        claude.gaps.append("Add JSON-LD schema")
    if len(h1_tags) + len(h2_tags) >= 3:
        claude.signals.append("Good heading hierarchy")
        claude.score += 25
    else:
        claude.gaps.append("Improve heading structure")
    if has_canonical:
        claude.signals.append("Canonical URL present")
        claude.score += 25
    else:
        claude.gaps.append("Add canonical URL")
    results["Claude"] = claude

    return results


def format_platform_report(results: dict[str, PlatformResult]) -> str:
    """Format platform check results as text report."""
    lines = ["Platform Readiness Report", "=" * 40, ""]

    for name, result in sorted(results.items(), key=lambda x: -x[1].score):
        indicator = "🟢" if result.score >= 70 else "🟡" if result.score >= 40 else "🔴"
        lines.append(f"{indicator} {name}: {result.score}/100")
        for sig in result.signals:
            lines.append(f"   ✅ {sig}")
        for gap in result.gaps:
            lines.append(f"   ❌ {gap}")
        lines.append("")

    return "\n".join(lines)
