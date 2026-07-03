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

### 知识库

- [踩坑合集](https://vcnvmnln7wit.feishu.cn/wiki/CjV9wG8IHiIpWikCdFEcxfErnne)
- [商业化案例库](https://vcnvmnln7wit.feishu.cn/wiki/LdIxwlrKGibFEVkWMocc2K9KnBh)
- [科普专栏](https://vcnvmnln7wit.feishu.cn/wiki/K1RPwM8zji9ZchkxlOmcivUgnJe)
- [Open Build](https://vcnvmnln7wit.feishu.cn/wiki/CThswol0PiNJJbkhgT1cZIxanLb)
- [LLM/Agent/研究报告知识库](https://vcnvmnln7wit.feishu.cn/wiki/KwGQwS2TciT2EdkSBBtcYnbsnSd)
- [Skill封装合集](https://vcnvmnln7wit.feishu.cn/wiki/PDfpwqJZUibTyBkUa7TcZZ6Onpd)
- [社区治理运营知识库](https://vcnvmnln7wit.feishu.cn/wiki/MSEGwrdnTiiF9Dk8qCVcNW6InJg)

### 加入社群

| 社群 | 链接 |
|------|------|
| AI探索交流1区 | [加入](https://applink.feishu.cn/client/chat/chatter/add_by_link?link_token=074vd565-6084-455c-ac52-9703e89a0697) |
| AI探索交流2区 | [加入](https://applink.feishu.cn/client/chat/chatter/add_by_link?link_token=60bj94f0-1a67-48a7-abbb-9172b161c2b0) |
| AI探索交流3区 | [加入](https://applink.feishu.cn/client/chat/chatter/add_by_link?link_token=13do1920-db46-4444-b635-005680beaf58) |
| AI探索交流4区 | [加入](https://applink.feishu.cn/client/chat/chatter/add_by_link?link_token=f17o1b86-06f6-4f10-911a-69a299a25fe3) |
| AI探索交流5区 | [加入](https://applink.feishu.cn/client/chat/chatter/add_by_link?link_token=2bbh6ab6-22c2-4753-b973-74bb1a2edcc9) |
| AI探索交流6区 | [加入](https://applink.feishu.cn/client/chat/chatter/add_by_link?link_token=d19r19f7-2f47-42ba-b1ec-cb0342cf2e80) |
| AI探索交流7区 | [加入](https://applink.feishu.cn/client/chat/chatter/add_by_link?link_token=fe9vdacc-7316-4b4d-ae4a-fdbcf56315e6) |
| AI探索交流8区 | [加入](https://applink.feishu.cn/client/chat/chatter/add_by_link?link_token=103kfae8-1fd7-424f-984f-d66c210e42d1) |
| AI探索交流9区 | [加入](https://applink.feishu.cn/client/chat/chatter/add_by_link?link_token=239p3cad-2f83-4baa-a230-f40386067548) |
| AI探索交流10区 | [加入](https://applink.feishu.cn/client/chat/chatter/add_by_link?link_token=880r7cf5-3638-45ff-afb9-7944de991872) |
| AI探索交流-网文作家 | [加入](https://applink.feishu.cn/client/chat/chatter/add_by_link?link_token=6a3v579b-ab43-4e1a-87f9-be63bab88da7) |
| AI探索交流群-音乐达人 | [加入](https://applink.feishu.cn/client/chat/chatter/add_by_link?link_token=76at299e-73da-4eeb-9eba-32161e98f2f8) |
| AI探索交流群-微笑驿站 | [加入](https://applink.feishu.cn/client/chat/chatter/add_by_link?link_token=f2av73d0-6bb4-4a9f-9095-5fbbe83e49ec) |

---

*AtomCollide-智械工坊团队出品*

---

## 组织与社群入口

**元素碰撞 · AtomCollide-AI 智能体实验室**：面向学习者、创作者与自动化实践者，持续沉淀可复用的 AI Agent 产品、工作流与工程经验。使命：**for the learner**。

> 请选择 1 个常用社群加入，内容全域同步，无需重复加入。

### 知识库

| 知识库 | 链接 |
|---|---|
| 踩坑合集 | [进入](https://vcnvmnln7wit.feishu.cn/wiki/CjV9wG8IHiIpWikCdFEcxfErnne) |
| 商业化案例库 | [进入](https://vcnvmnln7wit.feishu.cn/wiki/LdIxwlrKGibFEVkWMocc2K9KnBh) |
| 科普专栏 | [进入](https://vcnvmnln7wit.feishu.cn/wiki/K1RPwM8zji9ZchkxlOmcivUgnJe) |
| Open Build | [进入](https://vcnvmnln7wit.feishu.cn/wiki/CThswol0PiNJJbkhgT1cZIxanLb) |
| LLM / Agent / 研究报告 | [进入](https://vcnvmnln7wit.feishu.cn/wiki/KwGQwS2TciT2EdkSBBtcYnbsnSd) |
| Skill 封装合集 | [进入](https://vcnvmnln7wit.feishu.cn/wiki/PDfpwqJZUibTyBkUa7TcZZ6Onpd) |
| 社区治理运营 | [进入](https://vcnvmnln7wit.feishu.cn/wiki/MSEGwrdnTiiF9Dk8qCVcNW6InJg) |

### 社群邀请

| 社群 | 链接 |
|---|---|
| AI 探索交流 1 区 | [加入](https://applink.feishu.cn/client/chat/chatter/add_by_link?link_token=074vd565-6084-455c-ac52-9703e89a0697) |
| AI 探索交流 2 区 | [加入](https://applink.feishu.cn/client/chat/chatter/add_by_link?link_token=60bj94f0-1a67-48a7-abbb-9172b161c2b0) |
| AI 探索交流 3 区 | [加入](https://applink.feishu.cn/client/chat/chatter/add_by_link?link_token=13do1920-db46-4444-b635-005680beaf58) |
| AI 探索交流 4 区 | [加入](https://applink.feishu.cn/client/chat/chatter/add_by_link?link_token=f17o1b86-06f6-4f10-911a-69a299a25fe3) |
| AI 探索交流 5 区 | [加入](https://applink.feishu.cn/client/chat/chatter/add_by_link?link_token=2bbh6ab6-22c2-4753-b973-74bb1a2edcc9) |
| AI 探索交流 6 区 | [加入](https://applink.feishu.cn/client/chat/chatter/add_by_link?link_token=d19r19f7-2f47-42ba-b1ec-cb0342cf2e80) |
| AI 探索交流 7 区 | [加入](https://applink.feishu.cn/client/chat/chatter/add_by_link?link_token=fe9vdacc-7316-4b4d-ae4a-fdbcf56315e6) |
| AI 探索交流 8 区 | [加入](https://applink.feishu.cn/client/chat/chatter/add_by_link?link_token=103kfae8-1fd7-424f-984f-d66c210e42d1) |
| AI 探索交流 9 区 | [加入](https://applink.feishu.cn/client/chat/chatter/add_by_link?link_token=239p3cad-2f83-4baa-a230-f40386067548) |
| AI 探索交流 10 区 | [加入](https://applink.feishu.cn/client/chat/chatter/add_by_link?link_token=880r7cf5-3638-45ff-afb9-7944de991872) |
| AI 探索交流 — 网文作家 | [加入](https://applink.feishu.cn/client/chat/chatter/add_by_link?link_token=6a3v579b-ab43-4e1a-87f9-be63bab88da7) |
| AI 探索交流群 — 音乐达人 | [加入](https://applink.feishu.cn/client/chat/chatter/add_by_link?link_token=76at299e-73da-4eeb-9eba-32161e98f2f8) |
| AI 探索交流群 — 微笑驿站 | [加入](https://applink.feishu.cn/client/chat/chatter/add_by_link?link_token=f2av73d0-6bb4-4a9f-9095-5fbbe83e49ec) |

---

AtomCollide-智械工坊团队出品。更多产品见：[AtomCollide Product Matrix](https://503496348-ops.github.io/atomcollide-product-matrix/)。


## 示例输出

本仓库的最小可验证使用路径：

1. 阅读 README 的 Quick Start / 使用说明，完成本地安装或配置。
2. 按仓库提供的命令、脚本或入口运行一次最小任务。
3. 对照本产品定位验证输出：**意识浓缩（Minddistill）** 属于 **GEO诊断** 产品，目标是把输入材料转化为可检查、可复用的结果。
4. 若运行环境暂不可用，先通过 README、CHANGELOG、CI 状态和源码结构完成静态验收，再补充真实截图或录屏。

> 维护要求：后续每次发布都应把真实运行截图、CLI 输出、网页截图或 API 响应样例补充到本节，避免仓库首页只描述能力、不展示结果。

## Governance Links

- [LICENSE](LICENSE)
- [CHANGELOG](CHANGELOG.md)
- [SECURITY](SECURITY.md)
- [CONTRIBUTING](CONTRIBUTING.md)

## 2026-07-03 产品收敛门禁

- 新增 `scripts/product_convergence_gate.py`：从远端干净 clone 后可运行 `python3 scripts/product_convergence_gate.py --json`，检查 SKILL/README、入口文件、smoke 目标、测试与外部融合引用是否自洽。
- 新增 `tests/test_product_convergence_gate.py`：确保门禁在产品仓库中真实可执行，避免后续增强只停留在孤岛模块。
