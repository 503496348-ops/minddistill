"""GEO Campaign — 从审计到投放的完整闭环。

生成推广内容 → 多渠道投放 → 效果追踪

基于minddistill审计结果，自动生成：
- 社群推广文案（飞书/微信/Telegram）
- 技术博客文章
- 社交媒体帖子（X/Twitter）
- 落地页HTML
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class CampaignContent:
    """推广内容集合。"""
    title: str
    summary: str  # 一句话摘要
    feishu_post: str  # 飞书社群帖子
    blog_article: str  # 技术博客文章
    social_posts: dict[str, str]  # 平台->帖子内容
    landing_html: str  # 落地页HTML
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class CampaignMetrics:
    """推广效果指标。"""
    channel: str
    views: int = 0
    clicks: int = 0
    conversions: int = 0
    engagement_rate: float = 0.0
    recorded_at: str = field(default_factory=lambda: datetime.now().isoformat())


def generate_campaign_from_audit(
    audit_result,
    site_name: str,
    site_url: str,
    product_tagline: str = "",
    target_audience: str = "SEO从业者、内容创作者、技术团队",
    campaign_goal: str = "推广minddistill GEO诊断工具",
) -> CampaignContent:
    """从审计结果生成完整推广内容。

    Args:
        audit_result: GeoAuditResult对象
        site_name: 被审计网站名称
        site_url: 被审计网站URL
        product_tagline: 产品标语
        target_audience: 目标受众
        campaign_goal: 推广目标
    """
    # 提取关键数据
    score = audit_result.overall_score
    band = audit_result.score_band
    weak_dims = []
    strong_dims = []

    for dim in audit_result.dimensions:
        if dim.score < 50:
            weak_dims.append((dim.name, dim.score))
        elif dim.score >= 80:
            strong_dims.append((dim.name, dim.score))

    weak_dims.sort(key=lambda x: x[1])
    strong_dims.sort(key=lambda x: x[1], reverse=True)

    # 生成标题
    title = f"🧠 {site_name} GEO诊断报告：{score}/100分，AI搜索引擎就绪度{'优秀' if score >= 80 else '待优化' if score >= 50 else '急需提升'}"

    # 生成摘要
    summary = f"我们用Minddistill对{site_name}进行了8维度GEO审计，总分{score}/100 [{band}]。"
    if weak_dims:
        summary += f"主要短板：{weak_dims[0][0]}({weak_dims[0][1]}分)。"
    summary += f"立即查看完整诊断报告和优化方案。"

    # 生成飞书社群帖子
    feishu_post = _generate_feishu_post(
        site_name, site_url, score, band, weak_dims, strong_dims,
        product_tagline, target_audience
    )

    # 生成博客文章
    blog_article = _generate_blog_article(
        site_name, site_url, score, band, weak_dims, strong_dims,
        audit_result, product_tagline
    )

    # 生成社交媒体帖子
    social_posts = _generate_social_posts(
        site_name, site_url, score, band, weak_dims, product_tagline
    )

    # 生成落地页HTML
    landing_html = _generate_landing_html(
        site_name, site_url, score, band, weak_dims, strong_dims,
        product_tagline, target_audience
    )

    return CampaignContent(
        title=title,
        summary=summary,
        feishu_post=feishu_post,
        blog_article=blog_article,
        social_posts=social_posts,
        landing_html=landing_html,
    )


def _generate_feishu_post(
    site_name: str, site_url: str,
    score: int, band: str,
    weak_dims: list, strong_dims: list,
    tagline: str, audience: str,
) -> str:
    """生成飞书社群推广帖子。"""
    lines = [
        f"## 🧠 {site_name} GEO诊断报告",
        f"",
        f"**总分：{score}/100 [{band.upper()}]**",
        f"",
        f"### 📊 维度分析",
        f"",
    ]

    # 弱项
    if weak_dims:
        lines.append("**🔴 待优化：**")
        for name, score in weak_dims[:3]:
            lines.append(f"- {name}: {score}/100")
        lines.append("")

    # 强项
    if strong_dims:
        lines.append("**🟢 表现优秀：**")
        for name, score in strong_dims[:3]:
            lines.append(f"- {name}: {score}/100")
        lines.append("")

    lines.extend([
        f"### 🔧 优化建议",
        f"",
        f"使用 **Minddistill GEO诊断引擎** 一键生成修复方案：",
        f"```bash",
        f"python3 engine.py {site_url} --fix --site-name '{site_name}' --site-desc '...'",
        f"```",
        f"",
        f"自动生成：",
        f"- robots.txt（AI爬虫规则）",
        f"- llms.txt（AI站点描述）",
        f"- JSON-LD结构化数据",
        f"- Meta标签优化",
        f"",
        f"### 💡 适用人群",
        f"",
        f"{audience}",
        f"",
        f"---",
        f"*{tagline or 'Minddistill — AI搜索引擎就绪度诊断引擎'}*",
        f"",
        f"🔗 GitHub: https://github.com/503496348-ops/minddistill",
    ])

    return "\n".join(lines)


def _generate_blog_article(
    site_name: str, site_url: str,
    score: int, band: str,
    weak_dims: list, strong_dims: list,
    audit_result, tagline: str,
) -> str:
    """生成技术博客文章。"""
    lines = [
        f"# {site_name} GEO诊断报告：如何让AI搜索引擎更好地引用你的内容",
        f"",
        f"> 本文使用Minddistill GEO诊断引擎对{site_url}进行了全面的AI搜索引擎就绪度审计。",
        f"",
        f"## 背景",
        f"",
        f"随着ChatGPT Search、Perplexity、Google AI Overviews等AI搜索引擎的崛起，",
        f"传统的SEO策略已经不足以确保你的内容被AI发现和引用。",
        f"Generative Engine Optimization (GEO) 成为新的必修课。",
        f"",
        f"## 审计结果",
        f"",
        f"**{site_name} 获得了 {score}/100 的GEO评分，评级为 {band.upper()}。**",
        f"",
        f"| 维度 | 分数 | 状态 |",
        f"|------|------|------|",
    ]

    for dim in sorted(audit_result.dimensions, key=lambda d: d.score):
        status = "✅" if dim.score >= 70 else "⚠️" if dim.score >= 40 else "❌"
        lines.append(f"| {dim.name} | {dim.score}/100 | {status} |")

    lines.extend([
        f"",
        f"## 关键发现",
        f"",
    ])

    if weak_dims:
        lines.append("### 需要改进的领域")
        lines.append("")
        for name, score in weak_dims:
            lines.append(f"**{name} ({score}/100)**")
            # 找到对应的维度建议
            for dim in audit_result.dimensions:
                if dim.name == name:
                    for rec in dim.recommendations:
                        lines.append(f"- {rec}")
            lines.append("")

    if strong_dims:
        lines.append("### 表现优秀的领域")
        lines.append("")
        for name, score in strong_dims:
            lines.append(f"**{name} ({score}/100)**")
            for dim in audit_result.dimensions:
                if dim.name == name:
                    for finding in dim.findings[:2]:
                        lines.append(f"- {finding}")
            lines.append("")

    lines.extend([
        f"## 优化方案",
        f"",
        f"使用Minddistill GEO诊断引擎，可以一键生成修复文件：",
        f"",
        f"```bash",
        f"python3 engine.py {site_url} --fix --site-name '{site_name}' --site-desc '...'",
        f"```",
        f"",
        f"生成的文件包括：",
        f"- **robots.txt** — 允许AI爬虫访问",
        f"- **llms.txt** — 向AI描述你的站点",
        f"- **JSON-LD** — 结构化数据，帮助AI理解内容",
        f"- **Meta标签** — 优化社交分享和AI抓取",
        f"",
        f"## 结论",
        f"",
        f"GEO不是替代SEO，而是SEO的扩展。通过优化技术信号和内容结构，",
        f"你可以显著提升在AI搜索引擎中的可见度和被引用概率。",
        f"",
        f"---",
        f"",
        f"*{tagline or 'Minddistill — AI搜索引擎就绪度诊断引擎'}*",
        f"",
        f"GitHub: https://github.com/503496348-ops/minddistill",
    ])

    return "\n".join(lines)


def _generate_social_posts(
    site_name: str, site_url: str,
    score: int, band: str,
    weak_dims: list, tagline: str,
) -> dict[str, str]:
    """生成各平台社交媒体帖子。"""
    posts = {}

    # X/Twitter (280字符限制)
    weak_str = weak_dims[0][0] if weak_dims else "多项指标"
    posts["twitter"] = (
        f"🧠 {site_name} GEO诊断：{score}/100分\n\n"
        f"AI搜索引擎能发现你的内容吗？\n\n"
        f"主要短板：{weak_str}\n\n"
        f"用Minddistill一键诊断+修复 👇\n"
        f"https://github.com/503496348-ops/minddistill\n\n"
        f"#GEO #SEO #AISearch #ContentMarketing"
    )

    # 小红书
    posts["xiaohongshu"] = (
        f"🧠 {site_name}网站体检报告来了！\n\n"
        f"GEO评分：{score}/100 {'✨优秀' if score >= 80 else '⚠️待优化' if score >= 50 else '❌急需提升'}\n\n"
        f"什么是GEO？\n"
        f"就是让ChatGPT、Perplexity这些AI搜索引擎\n"
        f"能找到你的内容、理解你的内容、引用你的内容！\n\n"
        f"主要问题：{weak_str}\n\n"
        f"好消息是：有工具可以一键诊断+自动生成修复方案！\n\n"
        f"评论区扣「GEO」获取工具链接～\n\n"
        f"#SEO #GEO #AI搜索 #网站优化 #内容营销 #数字营销"
    )

    # 微信公众号
    posts["wechat"] = (
        f"【{site_name}网站GEO诊断报告】\n\n"
        f"AI搜索引擎时代，你的网站准备好了吗？\n\n"
        f"我们用GEO诊断引擎对{site_name}进行了8维度审计：\n"
        f"- 总分：{score}/100\n"
        f"- 评级：{band.upper()}\n"
        f"- 主要短板：{weak_str}\n\n"
        f"什么是GEO？\n"
        f"Generative Engine Optimization，即生成式搜索引擎优化。\n"
        f"目的是让你的内容更容易被ChatGPT、Perplexity等AI搜索引擎发现和引用。\n\n"
        f"回复「诊断」获取免费GEO审计工具。"
    )

    # 知乎
    posts["zhihu"] = (
        f"# {site_name}的GEO诊断报告：AI搜索引擎就绪度分析\n\n"
        f"## 什么是GEO？\n\n"
        f"GEO（Generative Engine Optimization）是针对AI搜索引擎的优化策略。\n"
        f"随着ChatGPT Search、Perplexity、Google AI Overviews的普及，\n"
        f"传统SEO已经不够了——你需要让AI「理解」你的内容。\n\n"
        f"## {site_name}的诊断结果\n\n"
        f"总分：{score}/100 [{band.upper()}]\n\n"
        f"主要短板：{weak_str}\n\n"
        f"## 如何优化？\n\n"
        f"1. 检查robots.txt是否允许AI爬虫\n"
        f"2. 添加llms.txt描述你的站点\n"
        f"3. 使用JSON-LD结构化数据\n"
        f"4. 优化内容的可引用性\n\n"
        f"完整工具和方法见文末链接。"
    )

    return posts


def _generate_landing_html(
    site_name: str, site_url: str,
    score: int, band: str,
    weak_dims: list, strong_dims: list,
    tagline: str, audience: str,
) -> str:
    """生成推广落地页HTML。"""
    score_color = "#22c55e" if score >= 80 else "#eab308" if score >= 50 else "#ef4444"

    weak_html = ""
    if weak_dims:
        for name, s in weak_dims[:3]:
            weak_html += f"""
            <div class="dimension weak">
                <span class="dim-name">{name}</span>
                <span class="dim-score">{s}/100</span>
                <div class="dim-bar">
                    <div class="dim-fill" style="width: {s}%; background: #ef4444;"></div>
                </div>
            </div>"""

    strong_html = ""
    if strong_dims:
        for name, s in strong_dims[:3]:
            strong_html += f"""
            <div class="dimension strong">
                <span class="dim-name">{name}</span>
                <span class="dim-score">{s}/100</span>
                <div class="dim-bar">
                    <div class="dim-fill" style="width: {s}%; background: #22c55e;"></div>
                </div>
            </div>"""

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{site_name} GEO诊断报告 - Minddistill</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #e2e8f0;
            min-height: 100vh;
            padding: 2rem;
        }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        .header {{ text-align: center; margin-bottom: 3rem; }}
        .header h1 {{ font-size: 2.5rem; margin-bottom: 0.5rem; }}
        .header .subtitle {{ color: #94a3b8; font-size: 1.1rem; }}
        .score-card {{
            background: rgba(255,255,255,0.05);
            border-radius: 1rem;
            padding: 2rem;
            text-align: center;
            margin-bottom: 2rem;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        .score {{ font-size: 5rem; font-weight: bold; color: {score_color}; }}
        .band {{ font-size: 1.5rem; color: #94a3b8; text-transform: uppercase; }}
        .dimensions {{ margin-bottom: 2rem; }}
        .dimension {{
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1rem;
            padding: 1rem;
            background: rgba(255,255,255,0.03);
            border-radius: 0.5rem;
        }}
        .dim-name {{ flex: 1; font-weight: 500; }}
        .dim-score {{ min-width: 60px; text-align: right; }}
        .dim-bar {{
            width: 100px;
            height: 8px;
            background: rgba(255,255,255,0.1);
            border-radius: 4px;
            overflow: hidden;
        }}
        .dim-fill {{ height: 100%; border-radius: 4px; }}
        .cta {{
            text-align: center;
            margin-top: 3rem;
        }}
        .btn {{
            display: inline-block;
            padding: 1rem 2rem;
            background: #3b82f6;
            color: white;
            text-decoration: none;
            border-radius: 0.5rem;
            font-weight: 600;
            transition: background 0.2s;
        }}
        .btn:hover {{ background: #2563eb; }}
        .footer {{
            text-align: center;
            margin-top: 3rem;
            color: #64748b;
            font-size: 0.9rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 {site_name}</h1>
            <p class="subtitle">GEO诊断报告 · AI搜索引擎就绪度审计</p>
        </div>

        <div class="score-card">
            <div class="score">{score}</div>
            <div class="band">{band}</div>
        </div>

        <div class="dimensions">
            <h2>📊 维度分析</h2>
            {weak_html}
            {strong_html}
        </div>

        <div class="cta">
            <h2>🔧 立即优化</h2>
            <p style="margin: 1rem 0; color: #94a3b8;">
                使用Minddistill一键生成修复方案
            </p>
            <a href="https://github.com/503496348-ops/minddistill" class="btn">
                获取Minddistill →
            </a>
        </div>

        <div class="footer">
            <p>{tagline or 'Minddistill — AI搜索引擎就绪度诊断引擎'}</p>
            <p>AtomCollide-智械工坊团队出品</p>
        </div>
    </div>
</body>
</html>"""

    return html


def save_campaign(content: CampaignContent, output_dir: str = "./geo-campaign"):
    """保存推广内容到文件。"""
    from pathlib import Path

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    saved = []

    # 保存飞书帖子
    p = Path(output_dir) / "feishu-post.md"
    p.write_text(content.feishu_post, encoding="utf-8")
    saved.append(str(p))

    # 保存博客文章
    p = Path(output_dir) / "blog-article.md"
    p.write_text(content.blog_article, encoding="utf-8")
    saved.append(str(p))

    # 保存社交媒体帖子
    for platform, post in content.social_posts.items():
        p = Path(output_dir) / f"social-{platform}.txt"
        p.write_text(post, encoding="utf-8")
        saved.append(str(p))

    # 保存落地页
    p = Path(output_dir) / "landing-page.html"
    p.write_text(content.landing_html, encoding="utf-8")
    saved.append(str(p))

    # 保存元数据
    meta = {
        "title": content.title,
        "summary": content.summary,
        "created_at": content.created_at,
        "files": saved,
    }
    p = Path(output_dir) / "campaign-meta.json"
    p.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    saved.append(str(p))

    return saved
