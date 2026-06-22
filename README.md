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

---

## 🚀 加入AtomCollide-AI智能体实验室

**元素碰撞-AtomCollide-AI 智能体实验室** 是一个专注于AI领域的开源组织，汇聚了众多优秀学习者。

### 核心价值

**找工作：更省力，也更精准**
- 一线大厂内推通道（字节、阿里、腾讯等）
- 全链路求职赋能包（面试题库、简历优化、晋升指导）
- 线下技术沙龙 & 人脉网络

**学AI测试：真正落地，拒绝空谈**
- 从0到1实战落地体系（Skills、MCP、RAG、AI IDE等）
- 独家自研资料与工具矩阵
- 前沿技术同步与提效方案

### 加入社群

- [知识库入口](https://vcnvmnln7wit.feishu.cn/wiki/WpK2wAcV8i6P8tke8X9cLcmDnSh)
- [AI探索交流群](https://applink.feishu.cn/client/chat/chatter/add_by_link?link_token=074vd565-6084-455c-ac52-9703e89a0697)

---

*AtomCollide-智械工坊团队出品*

