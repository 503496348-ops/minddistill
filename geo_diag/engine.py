"""GEO Diagnostic Report Engine — Main audit orchestrator.

Runs a comprehensive GEO audit on a website, scoring across 8 dimensions:
1. Robots.txt (AI crawler access)
2. llms.txt (AI site description)
3. Schema/JSON-LD (structured data)
4. Meta tags (title, description, OG, Twitter)
5. Content citability (AI extractability)
6. Platform readiness (ChatGPT/Perplexity/Gemini/Claude)
7. Brand entity signals
8. Technical SEO basics

Returns a GeoAuditResult with per-dimension scores and an overall 0-100 score.
"""

import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

# Optional imports with fallbacks
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False


@dataclass
class DimensionScore:
    """Score for a single audit dimension."""
    name: str
    score: int  # 0-100
    weight: float  # contribution to overall score
    findings: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)


@dataclass
class GeoAuditResult:
    """Complete GEO audit result."""
    url: str
    overall_score: int  # 0-100
    score_band: str  # critical/foundation/good/excellent
    dimensions: list[DimensionScore] = field(default_factory=list)
    page_title: str = ""
    page_description: str = ""
    ai_crawlers_blocked: list[str] = field(default_factory=list)
    ai_crawlers_allowed: list[str] = field(default_factory=list)
    has_llms_txt: bool = False
    has_schema_markup: bool = False
    schema_types: list[str] = field(default_factory=list)
    citability_score: int = 0
    platform_readiness: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        d = asdict(self)
        return d

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


# ── Fetch helpers ────────────────────────────────────────────────────

def _fetch_page(url: str, timeout: int = 15) -> Optional[str]:
    """Fetch a URL and return HTML content."""
    if not HAS_REQUESTS:
        return None
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; GEOAuditBot/1.0)",
            "Accept": "text/html",
        }
        resp = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        resp.raise_for_status()
        return resp.text
    except Exception:
        return None


def _fetch_robots_txt(base_url: str) -> Optional[str]:
    """Fetch robots.txt content."""
    robots_url = f"{base_url.rstrip('/')}/robots.txt"
    if not HAS_REQUESTS:
        return None
    try:
        resp = requests.get(robots_url, timeout=10)
        return resp.text if resp.status_code == 200 else None
    except Exception:
        return None


def _fetch_llms_txt(base_url: str) -> Optional[str]:
    """Fetch llms.txt content."""
    llms_url = f"{base_url.rstrip('/')}/llms.txt"
    if not HAS_REQUESTS:
        return None
    try:
        resp = requests.get(llms_url, timeout=10)
        return resp.text if resp.status_code == 200 else None
    except Exception:
        return None


# ── Dimension auditors ───────────────────────────────────────────────

AI_BOTS = {
    "OAI-SearchBot": "ChatGPT Search",
    "PerplexityBot": "Perplexity",
    "ClaudeBot": "Claude",
    "Google-Extended": "Gemini AI Overviews",
    "GPTBot": "GPT Training",
    "anthropic-ai": "Anthropic Training",
}


def _audit_robots(base_url: str) -> DimensionScore:
    """Audit robots.txt for AI crawler access."""
    ds = DimensionScore(name="robots.txt", score=0, weight=0.15)
    content = _fetch_robots_txt(base_url)

    if content is None:
        ds.findings.append("robots.txt not found or unreachable")
        ds.recommendations.append("Create a robots.txt file with appropriate AI bot rules")
        ds.score = 20
        return ds

    ds.findings.append("robots.txt found")

    blocked = []
    allowed = []

    for bot, platform in AI_BOTS.items():
        # Check if bot is explicitly disallowed
        pattern = re.compile(
            rf"(?:User-Agent:\s*{re.escape(bot)}\s*\n(?:[^\n]*\n)*?Disallow:\s*/)",
            re.IGNORECASE
        )
        if pattern.search(content):
            blocked.append(f"{bot} ({platform})")
        else:
            allowed.append(f"{bot} ({platform})")

    if blocked:
        ds.findings.append(f"Blocked AI crawlers: {', '.join(blocked)}")
        ds.recommendations.append(f"Allow these AI crawlers: {', '.join(blocked)}")
    if allowed:
        ds.findings.append(f"Allowed AI crawlers: {', '.join(allowed)}")

    # Score: 100 if all allowed, -15 per blocked bot
    ds.score = max(0, 100 - len(blocked) * 15)
    return ds


def _audit_llms_txt(base_url: str) -> DimensionScore:
    """Audit llms.txt presence and quality."""
    ds = DimensionScore(name="llms.txt", score=0, weight=0.10)
    content = _fetch_llms_txt(base_url)

    if content is None:
        ds.findings.append("llms.txt not found")
        ds.recommendations.append("Create an llms.txt file describing your site for AI crawlers")
        ds.score = 0
        return ds

    ds.findings.append("llms.txt found")
    lines = content.strip().split("\n")

    # Check structure
    has_h1 = any(l.startswith("# ") for l in lines)
    has_description = any(l.startswith("> ") for l in lines)
    has_sections = sum(1 for l in lines if l.startswith("## ")) >= 2
    line_count = len(lines)

    if has_h1:
        ds.findings.append("Has H1 site name")
    else:
        ds.recommendations.append("Add H1 heading with site name")

    if has_description:
        ds.findings.append("Has blockquote description")
    else:
        ds.recommendations.append("Add blockquote description after H1")

    if has_sections:
        ds.findings.append("Has multiple H2 sections")
    else:
        ds.recommendations.append("Add H2 sections with categorized links")

    if line_count > 200:
        ds.findings.append(f"llms.txt is {line_count} lines (recommended <200)")
        ds.recommendations.append("Trim llms.txt to under 200 lines")

    score = 30  # base for having the file
    if has_h1:
        score += 20
    if has_description:
        score += 20
    if has_sections:
        score += 20
    if line_count <= 200:
        score += 10
    ds.score = min(100, score)
    return ds


def _audit_schema(html: str) -> DimensionScore:
    """Audit JSON-LD schema markup."""
    ds = DimensionScore(name="Schema/JSON-LD", score=0, weight=0.12)

    if not HAS_BS4:
        ds.findings.append("BeautifulSoup not available, skipping schema check")
        ds.score = 50
        return ds

    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all("script", type="application/ld+json")
    schema_types = []

    for script in scripts:
        try:
            data = json.loads(script.string)
            if isinstance(data, dict):
                schema_types.append(data.get("@type", "Unknown"))
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        schema_types.append(item.get("@type", "Unknown"))
        except (json.JSONDecodeError, TypeError):
            pass

    if schema_types:
        ds.findings.append(f"Found schema types: {', '.join(schema_types)}")
        ds.score = min(100, 40 + len(schema_types) * 15)
    else:
        ds.findings.append("No JSON-LD schema markup found")
        ds.recommendations.append("Add JSON-LD schema (Organization, WebPage, Article, etc.)")
        ds.score = 10

    return ds


def _audit_meta(html: str) -> DimensionScore:
    """Audit meta tags (title, description, OG, Twitter)."""
    ds = DimensionScore(name="Meta Tags", score=0, weight=0.10)

    if not HAS_BS4:
        ds.findings.append("BeautifulSoup not available, skipping meta check")
        ds.score = 50
        return ds

    soup = BeautifulSoup(html, "html.parser")
    score = 0

    # Title
    title = soup.find("title")
    if title and title.string:
        ds.findings.append(f"Title: {title.string[:60]}")
        score += 25
    else:
        ds.findings.append("Missing <title> tag")
        ds.recommendations.append("Add a descriptive <title> tag")

    # Meta description
    desc = soup.find("meta", attrs={"name": "description"})
    if desc and desc.get("content"):
        ds.findings.append(f"Description: {desc['content'][:80]}")
        score += 25
    else:
        ds.findings.append("Missing meta description")
        ds.recommendations.append("Add meta description (120-160 chars)")

    # OG tags
    og_title = soup.find("meta", property="og:title")
    og_desc = soup.find("meta", property="og:description")
    if og_title or og_desc:
        ds.findings.append("Open Graph tags present")
        score += 25
    else:
        ds.findings.append("Missing Open Graph tags")
        ds.recommendations.append("Add og:title, og:description, og:image meta tags")

    # Twitter card
    twitter = soup.find("meta", attrs={"name": "twitter:card"})
    if twitter:
        ds.findings.append("Twitter Card tag present")
        score += 25
    else:
        ds.findings.append("Missing Twitter Card tag")
        ds.recommendations.append("Add twitter:card meta tag")

    ds.score = score
    return ds


def _audit_content_citability(html: str) -> DimensionScore:
    """Audit content for AI citability."""
    ds = DimensionScore(name="AI Citability", score=0, weight=0.18)

    if not HAS_BS4:
        ds.findings.append("BeautifulSoup not available, skipping citability check")
        ds.score = 50
        return ds

    soup = BeautifulSoup(html, "html.parser")

    # Remove scripts and styles
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    text = soup.get_text(separator="\n", strip=True)
    paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 50]

    if not paragraphs:
        ds.findings.append("No substantial content paragraphs found")
        ds.score = 10
        return ds

    # Score based on citability criteria (AI搜索优化研究)
    citable_count = 0
    for para in paragraphs:
        words = para.split()
        word_count = len(words)

        # Optimal length: 134-167 words
        length_ok = 100 <= word_count <= 200

        # Self-contained: starts with clear statement
        starts_clear = any(para.startswith(p) for p in [
            "According to", "The ", "A ", "In ", "This ", "Our ", "We ",
            "Based on", "Research", "Studies", "Data"
        ])

        # Fact-rich: contains numbers, percentages, dates
        has_stats = bool(re.search(r"\d+%|\d{4}|\$\d+|[\d,]+\s+(?:users|customers|people)", para))

        if length_ok and (starts_clear or has_stats):
            citable_count += 1

    citability_pct = (citable_count / len(paragraphs)) * 100 if paragraphs else 0
    ds.score = min(100, int(citability_pct * 1.5))

    ds.findings.append(f"Found {len(paragraphs)} content paragraphs")
    ds.findings.append(f"{citable_count} paragraphs meet AI citability criteria ({citability_pct:.0f}%)")

    if citability_pct < 30:
        ds.recommendations.append("Rewrite key paragraphs to be 134-167 words, self-contained, and fact-rich")
        ds.recommendations.append("Lead paragraphs with direct answers to common questions")
        ds.recommendations.append("Include specific statistics, dates, and named entities")

    return ds


def _audit_platform_readiness(html: str) -> DimensionScore:
    """Audit readiness for specific AI platforms."""
    ds = DimensionScore(name="Platform Readiness", score=0, weight=0.15)

    if not HAS_BS4:
        ds.score = 50
        return ds

    soup = BeautifulSoup(html, "html.parser")
    platforms = {}

    # ChatGPT Search readiness
    chatgpt_score = 0
    has_canonical = soup.find("link", rel="canonical") is not None
    has_schema = soup.find("script", type="application/ld+json") is not None
    has_meta_desc = soup.find("meta", attrs={"name": "description"}) is not None
    if has_canonical:
        chatgpt_score += 33
    if has_schema:
        chatgpt_score += 33
    if has_meta_desc:
        chatgpt_score += 34
    platforms["ChatGPT Search"] = chatgpt_score

    # Perplexity readiness
    perp_score = 0
    h1_tags = soup.find_all("h1")
    h2_tags = soup.find_all("h2")
    if h1_tags:
        perp_score += 30
    if len(h2_tags) >= 3:
        perp_score += 30
    if has_meta_desc:
        perp_score += 20
    if has_schema:
        perp_score += 20
    platforms["Perplexity"] = perp_score

    # Gemini AI Overviews
    gemini_score = 0
    if has_schema:
        gemini_score += 40
    if has_meta_desc:
        gemini_score += 30
    has_faq = bool(soup.find("script", type="application/ld+json", string=re.compile("FAQPage", re.I)))
    if has_faq:
        gemini_score += 30
    platforms["Gemini AI Overviews"] = gemini_score

    # Claude
    claude_score = 0
    if has_meta_desc:
        claude_score += 30
    if has_schema:
        claude_score += 30
    # Check for clear headings structure
    all_headings = soup.find_all(re.compile("^h[1-6]$"))
    if len(all_headings) >= 3:
        claude_score += 20
    if has_canonical:
        claude_score += 20
    platforms["Claude"] = claude_score

    for name, score in platforms.items():
        ds.findings.append(f"{name}: {score}/100 readiness")

    ds.score = int(sum(platforms.values()) / len(platforms))
    return ds


def _audit_brand_entity(html: str) -> DimensionScore:
    """Audit brand entity signals."""
    ds = DimensionScore(name="Brand Entity", score=0, weight=0.10)

    if not HAS_BS4:
        ds.score = 50
        return ds

    soup = BeautifulSoup(html, "html.parser")
    score = 0

    # Check for Organization schema
    scripts = soup.find_all("script", type="application/ld+json")
    has_org = False
    for script in scripts:
        try:
            data = json.loads(script.string)
            if isinstance(data, dict) and data.get("@type") == "Organization":
                has_org = True
                ds.findings.append("Organization schema found")
                score += 30
                break
        except (json.JSONDecodeError, TypeError):
            pass

    if not has_org:
        ds.recommendations.append("Add Organization JSON-LD schema")

    # Check for social links
    social_patterns = ["twitter.com", "linkedin.com", "github.com", "facebook.com"]
    social_found = []
    for link in soup.find_all("a", href=True):
        for pattern in social_patterns:
            if pattern in link["href"]:
                social_found.append(pattern.split(".")[0])

    if social_found:
        ds.findings.append(f"Social links: {', '.join(set(social_found))}")
        score += 20
    else:
        ds.recommendations.append("Add social media profile links")

    # Check for about/contact pages
    about_links = []
    for link in soup.find_all("a", href=True):
        href = link["href"].lower()
        if any(kw in href for kw in ["/about", "/contact", "/team"]):
            about_links.append(href)

    if about_links:
        ds.findings.append(f"About/Contact links found: {len(about_links)}")
        score += 20
    else:
        ds.recommendations.append("Add links to About and Contact pages")

    # Check for consistent branding in title and h1
    title = soup.find("title")
    h1 = soup.find("h1")
    if title and h1:
        title_text = (title.string or "").lower()
        h1_text = h1.get_text().lower()
        if any(word in title_text for word in h1_text.split()[:3]):
            score += 30
            ds.findings.append("Title and H1 are consistent")

    ds.score = min(100, score)
    return ds


def _audit_technical(html: str, url: str) -> DimensionScore:
    """Audit basic technical SEO signals."""
    ds = DimensionScore(name="Technical SEO", score=0, weight=0.10)

    if not HAS_BS4:
        ds.score = 50
        return ds

    soup = BeautifulSoup(html, "html.parser")
    score = 0

    # Canonical URL
    canonical = soup.find("link", rel="canonical")
    if canonical:
        ds.findings.append(f"Canonical: {canonical.get('href', '')[:60]}")
        score += 25
    else:
        ds.findings.append("Missing canonical URL")
        ds.recommendations.append("Add <link rel='canonical'> tag")

    # Viewport
    viewport = soup.find("meta", attrs={"name": "viewport"})
    if viewport:
        score += 25
    else:
        ds.findings.append("Missing viewport meta tag")

    # Lang attribute
    html_tag = soup.find("html")
    if html_tag and html_tag.get("lang"):
        score += 25
    else:
        ds.findings.append("Missing lang attribute on <html>")
        ds.recommendations.append("Add lang attribute to <html> tag")

    # HTTPS
    if url.startswith("https://"):
        score += 25
    else:
        ds.findings.append("Site not using HTTPS")
        ds.recommendations.append("Enable HTTPS")

    ds.score = score
    return ds


# ── Main audit orchestrator ──────────────────────────────────────────

def run_geo_audit(url: str, timeout: int = 15) -> GeoAuditResult:
    """Run a comprehensive GEO audit on a URL.

    Args:
        url: The URL to audit.
        timeout: HTTP request timeout in seconds.

    Returns:
        GeoAuditResult with per-dimension scores and overall 0-100 score.
    """
    if not HAS_REQUESTS:
        raise ImportError("requests package required: pip install requests")
    if not HAS_BS4:
        raise ImportError("beautifulsoup4 package required: pip install beautifulsoup4")

    # Normalize URL
    if not url.startswith("http"):
        url = "https://" + url

    parsed = urlparse(url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"

    # Fetch main page
    html = _fetch_page(url, timeout)
    if html is None:
        return GeoAuditResult(
            url=url, overall_score=0, score_band="critical",
            page_title="Failed to fetch page",
        )

    # Extract basic info
    soup = BeautifulSoup(html, "html.parser")
    title_tag = soup.find("title")
    desc_tag = soup.find("meta", attrs={"name": "description"})

    # Run all dimension audits
    dimensions = [
        _audit_robots(base_url),
        _audit_llms_txt(base_url),
        _audit_schema(html),
        _audit_meta(html),
        _audit_content_citability(html),
        _audit_platform_readiness(html),
        _audit_brand_entity(html),
        _audit_technical(html, url),
    ]

    # Calculate weighted overall score
    total_weight = sum(d.weight for d in dimensions)
    overall = int(sum(d.score * d.weight for d in dimensions) / total_weight) if total_weight > 0 else 0

    # Determine score band
    if overall <= 35:
        band = "critical"
    elif overall <= 67:
        band = "foundation"
    elif overall <= 85:
        band = "good"
    else:
        band = "excellent"

    # Build result
    result = GeoAuditResult(
        url=url,
        overall_score=overall,
        score_band=band,
        dimensions=dimensions,
        page_title=title_tag.string[:60] if title_tag and title_tag.string else "",
        page_description=desc_tag["content"][:120] if desc_tag and desc_tag.get("content") else "",
        has_llms_txt=any(d.name == "llms.txt" and d.score > 0 for d in dimensions),
        has_schema_markup=any(d.name == "Schema/JSON-LD" and d.score > 30 for d in dimensions),
        citability_score=next((d.score for d in dimensions if d.name == "AI Citability"), 0),
        platform_readiness={
            name: score
            for d in dimensions
            if d.name == "Platform Readiness"
            for finding in d.findings
            for name, score in [(finding.split(":")[0].strip(), int(finding.split(":")[1].strip().split("/")[0]))]
            if ":" in finding and "/" in finding
        },
    )

    return result


# ── Report formatter ─────────────────────────────────────────────────

def format_report_text(result: GeoAuditResult) -> str:
    """Format audit result as human-readable text report."""
    lines = []
    lines.append(f"{'='*60}")
    lines.append(f"GEO Diagnostic Report")
    lines.append(f"{'='*60}")
    lines.append(f"URL: {result.url}")
    lines.append(f"Title: {result.page_title}")
    lines.append(f"Overall Score: {result.overall_score}/100 [{result.score_band.upper()}]")
    lines.append("")

    # Score bar
    bar_len = 40
    filled = int(result.overall_score / 100 * bar_len)
    bar = "█" * filled + "░" * (bar_len - filled)
    lines.append(f"[{bar}] {result.overall_score}%")
    lines.append("")

    # Per-dimension breakdown
    lines.append(f"{'─'*60}")
    lines.append("Dimension Breakdown:")
    lines.append(f"{'─'*60}")

    for dim in sorted(result.dimensions, key=lambda d: d.score):
        indicator = "🟢" if dim.score >= 70 else "🟡" if dim.score >= 40 else "🔴"
        lines.append(f"  {indicator} {dim.name:25s} {dim.score:3d}/100 (weight: {dim.weight:.0%})")
        for finding in dim.findings[:3]:
            lines.append(f"     • {finding}")
        for rec in dim.recommendations[:1]:
            lines.append(f"     💡 {rec}")
        lines.append("")

    # Summary
    lines.append(f"{'─'*60}")
    lines.append("Key Recommendations:")
    lines.append(f"{'─'*60}")

    all_recs = []
    for dim in result.dimensions:
        for rec in dim.recommendations:
            if dim.score < 50:
                all_recs.append((dim.score, dim.name, rec))

    all_recs.sort()
    for i, (_, name, rec) in enumerate(all_recs[:5], 1):
        lines.append(f"  {i}. [{name}] {rec}")

    lines.append(f"\n{'='*60}")
    return "\n".join(lines)


# ── CLI ──────────────────────────────────────────────────────────────

def main():
    import argparse

    parser = argparse.ArgumentParser(description="GEO Diagnostic Report — Audit website AI search readiness")
    parser.add_argument("url", help="URL to audit")
    parser.add_argument("-o", "--output", help="Output file (text or JSON)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--timeout", type=int, default=15, help="HTTP timeout in seconds")

    args = parser.parse_args()

    print(f"🔍 Auditing {args.url}...")
    result = run_geo_audit(args.url, args.timeout)

    if args.json:
        output = result.to_json()
    else:
        output = format_report_text(result)

    print(output)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"\n📄 Report saved to {args.output}")


if __name__ == "__main__":
    main()
