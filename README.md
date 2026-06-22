# 意识浓缩 · Minddistill

> AI搜索引擎就绪度诊断引擎 — 8维度审计 + 可引用性评分 + 平台优化检测

作者：AtomCollide-智械工坊团队

## 快速开始

```bash
pip install requests beautifulsoup4
python3 geo_diag/engine.py https://example.com
python3 geo_diag/engine.py https://example.com --json -o report.json
```

## 8维度审计

| 维度 | 权重 | 说明 |
|------|------|------|
| robots.txt | 15% | AI爬虫(OAI-SearchBot/PerplexityBot/ClaudeBot/Google-Extended)访问权限 |
| llms.txt | 10% | AI站点描述文件结构和质量 |
| Schema/JSON-LD | 12% | 结构化数据类型和覆盖度 |
| Meta Tags | 10% | Title/Description/OG/Twitter Card |
| **AI Citability** | **18%** | 内容可引用性(段落长度/自包含性/事实密度) |
| Platform Readiness | 15% | ChatGPT/Perplexity/Gemini/Claude分别评分 |
| Brand Entity | 10% | Organization Schema+社交链接+品牌一致性 |
| Technical SEO | 10% | Canonical/Viewport/Lang/HTTPS |

## 评分标准

| 分数段 | 等级 | 含义 |
|--------|------|------|
| 0-35 | 🔴 Critical | 需要立即修复 |
| 36-67 | 🟡 Foundation | 基础框架已搭建 |
| 68-85 | 🟢 Good | 大部分优化到位 |
| 86-100 | 🟢 Excellent | 全面优化 |

## Python API

```python
from geo_diag import run_geo_audit, format_report_text
from geo_diag.platform_check import check_platform_readiness

result = run_geo_audit("https://example.com")
print(format_report_text(result))
print(f"Overall: {result.overall_score}/100 [{result.score_band}]")
```

## 许可证

MIT © AtomCollide-智械工坊团队
