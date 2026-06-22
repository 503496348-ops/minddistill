---
name: minddistill
description: >
  意识浓缩 · Minddistill — AI搜索引擎就绪度诊断引擎。
  8维度评分(robots.txt/llms.txt/Schema/Meta/可引用性/平台优化/品牌实体/技术SEO)。
  AI可引用性评分 + 4平台就绪度检测 + 自动生成修复文件。
triggers:
  - GEO审计
  - GEO诊断
  - AI搜索优化
  - 可引用性评分
  - geo audit
  - ai search readiness
  - 意识浓缩
  - minddistill
  - llms.txt
  - robots.txt审计
  - AI爬虫
  - 网站SEO诊断
  - GEO修复
  - 生成robots.txt
  - 生成llms.txt
version: "2.0"
---

# GEO 诊断报告引擎

> 8维度AI搜索引擎就绪度审计 + 可引用性评分 + 平台优化检测 + **自动生成修复文件**

## 核心能力

| 能力 | 说明 |
|------|------|
| 🔍 **审计** | 8维度评分，发现问题 |
| 🔧 **修复** | 自动生成robots.txt、llms.txt、JSON-LD、Meta标签 |
| 📊 **验证** | 修复前后对比，量化改进效果 |

## 使用方式

### 1. 仅审计（诊断模式）

```bash
python3 /root/.hermes/skills/minddistill/geo_diag/engine.py https://example.com
python3 /root/.hermes/skills/minddistill/geo_diag/engine.py https://example.com --json -o report.json
```

### 2. 审计 + 生成修复文件（闭环模式）

```bash
python3 /root/.hermes/skills/minddistill/geo_diag/engine.py https://example.com \
  --fix \
  --site-name "Your Site" \
  --site-desc "Your site description" \
  --fix-dir ./geo-fixes
```

生成的文件：
- `robots.txt` — AI爬虫规则
- `llms.txt` — AI站点描述
- `schema.jsonld` — 结构化数据（Organization + WebPage）
- `meta-tags.html` — OG/Twitter meta标签
- `head-snippet.html` — 完整`<head>`片段，可直接粘贴

### 3. 审计 + 修复 + 验证（完整闭环）

```bash
python3 /root/.hermes/skills/minddistill/geo_diag/engine.py https://example.com \
  --fix \
  --verify \
  --site-name "Your Site" \
  --site-desc "Your site description"
```

## Python API

```python
import sys
sys.path.insert(0, '/root/.hermes/skills/minddistill')
from geo_diag import run_geo_audit, format_report_text, generate_fixes_from_audit
from geo_diag.engine import GeoAuditResult
from geo_diag.fixer import GeoFixes

# 1. 审计
result: GeoAuditResult = run_geo_audit("https://example.com")
print(format_report_text(result))

# 2. 生成修复
fixes: GeoFixes = generate_fixes_from_audit(
    audit_result=result,
    site_name="Example",
    site_url="https://example.com",
    description="Example site description",
)
saved = fixes.save_all("./geo-fixes")
print(f"Generated {len(saved)} fix files")

# 3. 单独生成某个文件
from geo_diag import generate_robots_txt, generate_llms_txt, generate_jsonld_schema

robots = generate_robots_txt("https://example.com", allow_all_ai=True)
llms = generate_llms_txt("Example", "https://example.com", "Description here")
schema = generate_jsonld_schema("Example", "https://example.com", "Description")
```

## 8维度审计

| 维度 | 权重 | 说明 | 自动生成修复 |
|------|------|------|--------------|
| robots.txt | 15% | AI爬虫访问权限检查 | ✅ |
| llms.txt | 10% | AI站点描述文件检查 | ✅ |
| Schema/JSON-LD | 12% | 结构化数据评分 | ✅ |
| Meta Tags | 10% | Title/Description/OG/Twitter | ✅ |
| **AI Citability** | **18%** | 内容可引用性评分(Princeton KDD 2024) | ❌ 需人工优化 |
| Platform Readiness | 15% | ChatGPT/Perplexity/Gemini/Claude | ❌ 需人工优化 |
| Brand Entity | 10% | 品牌实体信号 | ⚠️ 部分可生成 |
| Technical SEO | 10% | 基础技术SEO | ⚠️ 部分可生成 |

## 实战价值

### 场景1：客户SEO审计
```bash
# 审计客户网站，生成诊断报告
python3 engine.py https://client-site.com --json -o audit.json

# 生成修复方案交付客户
python3 engine.py https://client-site.com --fix --site-name "Client" --site-desc "..." --fix-dir ./client-fixes
```

### 场景2：竞品GEO对比
```python
competitors = ['https://competitor1.com', 'https://competitor2.com']
for site in competitors:
    r = run_geo_audit(site)
    print(f"{site}: {r.overall_score}/100")
```

### 场景3：批量生成robots.txt/llms.txt
```python
from geo_diag import generate_robots_txt, generate_llms_txt

# 为客户批量生成
for client in clients:
    robots = generate_robots_txt(client['url'])
    llms = generate_llms_txt(client['name'], client['url'], client['desc'])
    # 保存或部署
```

## CLI参数

| 参数 | 说明 |
|------|------|
| `url` | 要审计的URL |
| `--json` | JSON格式输出 |
| `-o FILE` | 保存报告到文件 |
| `--fix` | 生成修复文件 |
| `--fix-dir DIR` | 修复文件保存目录（默认./geo-fixes） |
| `--verify` | 修复后重新审计对比 |
| `--site-name NAME` | 站点名称（--fix必填） |
| `--site-desc DESC` | 站点描述（--fix必填） |
| `--image-url URL` | OG图片URL（可选） |
| `--twitter HANDLE` | Twitter账号（可选） |

## 依赖

```bash
pip install requests beautifulsoup4
```

## 已知限制

- **部分网站屏蔽审计请求** — 如 openai.com 返回 0/100 (critical)，实际是请求被拒绝
- **AI Citability需人工优化** — 技术只能检测，无法自动改写内容
- **修复文件需部署** — 生成的文件需要上传到网站服务器才能生效

## 仓库

https://github.com/503496348-ops/minddistill

---

## ⚠️ Pitfalls

### Pitfall 1: 审计≠闭环（2026-06-22教训）

**错误模式**：只跑审计输出报告，不生成修复文件。用户原话："难道这个技能就只是验证？纯理论一点实战意义和价值都没？"

**正确做法**：
- 审计是**手段**，修复是**目的**
- 客户/用户要的是**解决方案**，不是**问题清单**
- 默认用`--fix`模式，除非用户明确说"只诊断"

**闭环流程**：
```
审计(发现问题) → 修复(生成文件) → 部署(上传服务器) → 验证(重新审计对比)
```

**每个环节的价值**：
1. 审计 → 知道问题在哪
2. 修复 → 知道怎么改
3. 部署 → 实际改了
4. 验证 → 证明有效

只有第1步没有第2-4步，等于医生只告诉你"你有病"但不开药。

### Pitfall 2: 生成文件≠自动部署

生成的修复文件保存在本地`--fix-dir`目录，**不会自动上传到网站**。
必须告诉用户：
1. 上传robots.txt和llms.txt到网站根目录
2. 将head-snippet.html内容添加到`<head>`标签内
3. 部署后再运行`--verify`验证效果

### Pitfall 3: --verify在修复前运行会显示"No change"

`--verify`重新审计同一URL，如果修复文件尚未部署，分数不会变化。
正确流程：生成修复 → 部署到网站 → 再运行验证。
