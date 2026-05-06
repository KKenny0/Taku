# Taku Case Studies

基于 Prove It 验证轮次的三个真实案例，展示 Taku 的纪律机制如何防止常见 AI coding 失败。

---

## Case 1: Debug — 阻止症状修复

### 场景

文件上传功能突然崩溃，抛出 `FileNotFoundError`。用户报告："昨天还好的，今天上传文件就崩了。"

### 没有 Taku

Agent 读取错误信息后，直接在崩溃点打补丁：

```python
# 症状修复 — 只在出错位置加了 fallback
path = config.get("upload_path") or "/tmp/uploads"
```

崩溃消失了。但根因（配置文件路径在最近提交中被改坏）没被找到。两天后，另一个依赖同一配置的功能也出了问题。

### 使用 Taku

`/taku-debug` 强制执行 4 阶段调查：

1. **INVESTIGATE** — 读取完整错误栈，追踪数据流，检查 `git diff HEAD~1`
2. **PATTERN** — 匹配"配置漂移"模式，搜索同代码库中的类似问题
3. **HYPOTHESIS** — 排序假设（H1: 路径变更 80%, H2: 权限变更 15%, H3: 环境差异 5%），逐个验证
4. **IMPLEMENT** — 先写回归测试，确认失败，再修复根因

产出 `DEBUG REPORT`，记录症状、根因、假设验证、修复内容和回归测试位置。回归测试确保同样的配置漂移不会被静默引入。

### 证据

Eval rt-01 retest（2026-05-06）：引入 mandatory sequence enforcement 后，agent 行为从"跳过调查直接修复"变为"产出 DEBUG REPORT + 回归测试 + Phase 1 完整调查"。4 turns, $0.21。

---

## Case 2: Review — SQL 注入不是"建议"

### 场景

Code review 阶段，diff 中出现字符串拼接构建的 SQL 查询。

### 没有 Taku

Agent 可能将 SQL 注入风险标记为 Informational 或 Medium severity — "建议使用参数化查询" — 但不阻止合并。开发者看到"建议"而非"阻塞"，大概率跳过。

更糟的情况：review 产出 30+ 条 findings（命名风格、注释格式、import 顺序…），SQL 注入被淹没在噪音里。开发者先修完 30 条 nit，然后合并了带 SQL 注入的代码。

### 使用 Taku

`/taku-review` 两轮审查：

- **Pass 1 (Critical)** — 识别 SQL injection risk，标记 **Critical**，引用 CWE-89
- **Auto-fix** — 直接提供参数化查询修复
- **阻止合并** — 输出 "Do not merge" 结论

同时发现资源泄漏（Medium）和 `SELECT *`（Low），但 Critical 优先处理，nit 控制在 2-3 条以内。信号不被噪音淹没。

### 证据

Eval rt-06（2026-05-05）：9 turns, $0.25。SQL 注入被标记为 Critical (CWE-89)，提供修复代码，未执行 commit/push/PR。Review 是 Taku 评估中表现最强的 skill。

---

## Case 3: Reflect — 拒绝编造趋势

### 场景

Sprint 回顾。Git 历史只有 7 次提交、4 天数据。

### 没有 Taku

Agent 为了让报告看起来更有价值，可能编造趋势分析：

- "团队 velocity 呈上升趋势" — 7 次提交不足以判断趋势
- "代码质量显著改善" — 没有任何质量指标支撑
- "Bug 修复效率提高" — 没有对比数据

这些编造的结论会误导后续 sprint 规划。

### 使用 Taku

`/taku-reflect`（Retro 模式）：

- 使用真实 git 数据（7 commits, 4 days, actual commit messages）
- **明确标注证据不足** — "当前数据不足以判断 velocity 趋势"
- **拒绝编造** — 不生成无支撑的结论
- 仍然给出可操作的改进建议（基于实际观察到的 commit pattern）

### 证据

Eval rt-08（2026-05-05）：29 turns, $0.85。Agent 使用真实 git 历史，显式声明数据限制，没有编造 velocity 趋势或质量判断。这是 Taku anti-rationalization 机制的核心价值：宁可报告"证据不足"，也不编造听起来专业的结论。

---

## 验证方法

这些案例来自 Taku Prove It 验证轮次：

- **9/10 programmatic evals** via `claude -p` — 覆盖全部 7 个 skills
- **1 interactive dogfood task** — 完整 Think → Plan → Build → Review 流程
- **结果** — 5 PASS, 3 PARTIAL, 0 FAIL, 1 SKIP + interactive all PASS
- **总成本** ~$6.11，平均每场景 ~$0.38

完整评估报告见 [`evals/evidence-report.md`](evals/evidence-report.md)。
