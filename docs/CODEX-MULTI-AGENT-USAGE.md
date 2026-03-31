# Codex 多代理协作使用指南

## 关键点（和 Claude 的差异）

Codex 的子代理是通过 `.codex/agents/*.toml` 定义的，不会像 Claude 的 agent 体系那样自动按组织结构“隐式编排”。

你需要在提示词里**显式指定子代理名和职责**，例如：

- `Have pr_explorer map impacted code paths, reviewer find risks, and docs_researcher verify APIs.`
- `Use game_designer to produce options, then gameplay_programmer to implement the selected option.`

## 启用与配置

1. 确保存在 `.codex/config.toml` 并设置：

```toml
[agents]
max_threads = 6
max_depth = 1
```

2. 项目内子代理定义放在 `.codex/agents/*.toml`。
3. 项目内技能放在 `.agents/skills/*/SKILL.md`。

## 推荐协作模式

### 模式 A：串行（最稳妥）

1. `explorer` / 只读代理先做代码与依赖映射。
2. 设计代理给出 2-3 方案与取舍。
3. 实现代理仅做最小修改。
4. QA/评审代理做回归检查。

### 模式 B：并行（高吞吐）

将任务拆成互不冲突的子域（如 UI、网络、AI），在同一轮提示中明确每个子代理边界，再由主代理统一汇总决策。

## 可直接复用的提示模板

### 1) Feature 协作

```
Implement feature X.
- Have game_designer propose 2 implementation options with tradeoffs.
- Have lead_programmer choose one architecture and list risks.
- Have gameplay_programmer implement minimal patch for the chosen option.
- Have qa_tester produce a focused test checklist.
Return a final merged plan before editing files.
```

### 2) Bug 修复协作

```
Investigate bug Y.
- Have pr_explorer map relevant code paths and probable root causes.
- Have reviewer identify correctness/security regressions.
- Have ui_programmer (or gameplay_programmer) implement the smallest safe fix.
- Have qa_tester define regression checks.
```

## 注意事项

- 代理名以 `.codex/agents/*.toml` 的 `name` 字段为准。
- 并行代理数量受 `[agents].max_threads` 限制。
- 避免过深递归（`max_depth` 建议保持 `1`），防止失控 fan-out。
