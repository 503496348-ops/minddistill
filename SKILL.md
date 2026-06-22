---
name: minddistill
description: >
  意识浓缩 · Minddistill — AI搜索引擎就绪度诊断引擎。
  8维度评分(robots.txt/llms.txt/Schema/Meta/可引用性/平台优化/品牌实体/技术SEO)。
  AI可引用性评分 + 4平台就绪度检测。
triggers:
  - GEO审计
  - GEO诊断
  - AI搜索优化
  - 可引用性评分
  - geo audit
  - ai search readiness
  - 意识浓缩
  - minddistill
version: "1.0"
---

# GEO 诊断报告引擎

> 8维度AI搜索引擎就绪度审计 + 可引用性评分 + 平台优化检测

## 使用方式

```bash
# CLI
python3 /root/.hermes/skills/minddistill/geo_diag/engine.py https://example.com
python3 /root/.hermes/skills/minddistill/geo_diag/engine.py https://example.com --json -o report.json

# Python API
from geo_diag import run_geo_audit, format_report_text
result = run_geo_audit("https://example.com")
print(format_report_text(result))
```

## 8维度审计

| 维度 | 权重 | 说明 |
|------|------|------|
| robots.txt | 15% | AI爬虫访问权限检查 |
| llms.txt | 10% | AI站点描述文件检查 |
| Schema/JSON-LD | 12% | 结构化数据评分 |
| Meta Tags | 10% | Title/Description/OG/Twitter |
| **AI Citability** | **18%** | 内容可引用性评分(Princeton KDD 2024) |
| Platform Readiness | 15% | ChatGPT/Perplexity/Gemini/Claude |
| Brand Entity | 10% | 品牌实体信号 |
| Technical SEO | 10% | 基础技术SEO |

## 依赖

```bash
pip install requests beautifulsoup4
```

## 仓库

https://github.com/503496348-ops/minddistill
