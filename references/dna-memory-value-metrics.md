# DNA Memory 价值度量融合

> 来源: [DNA Memory](https://github.com/AIPMAndy/dna-memory) — 记忆价值度量系统
> 融合目标: 记忆质量评分、认知分型诊断、召回效果度量

## 记忆价值指标

| 指标 | 含义 | 计算 |
|------|------|------|
| recall_attempts | 召回尝试次数 | 累计 |
| recall_hits | 命中次数 | 累计 |
| returned_memories | 返回记忆数 | 累计 |
| useful | 有用反馈数 | 累计 |
| misleading | 误导反馈数 | 累计 |
| new_memories | 新增记忆数 | 累计 |
| recall_share | 召回占比 | recall_hits / recall_attempts |

## 质量诊断维度

1. **召回命中率**: recall_hits / recall_attempts — 低=关键词提取需优化
2. **有用率**: useful / returned_memories — 低=记忆质量需提升
3. **误导率**: misleading / returned_memories — 高=记忆验证需加强
4. **认知新鲜度**: 最近写入时间 — 过旧=需要更新

## 认知分型诊断

按8种类型统计分布，识别：
- 偏好类过多 → 可能过度记录用户习惯
- 错误教训过少 → 可能遗漏重要失败经验
- 开放事项堆积 → 需要闭环清理
- 工作流类稀少 → 可复用流程未沉淀

## 诊断输出模板

```
记忆健康度: [A/B/C/D]
召回命中率: X%
有用率: X%
误导率: X%
认知分布: preference(N) fact(N) insight(N) decision(N) ...
建议: [具体优化建议]
```
