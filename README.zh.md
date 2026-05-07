<p align="center">
  <img src="logo.png" alt="Taku 琢" width="180" />
</p>

<h1 align="center">Taku 琢</h1>

<p align="center"><strong>面向 coding agent 的工程工作流 skills，用来控制 scope、上下文与交付质量。</strong></p>

<p align="center">
  <a href="README.md">English</a>
  ·
  <a href="#快速安装">快速安装</a>
  ·
  <a href="#核心工作流">核心工作流</a>
  ·
  <a href="#faq">FAQ</a>
</p>

<p align="center">
  <code>Scope Control</code> &nbsp;
  <code>TDD Build</code> &nbsp;
  <code>Real Diff Review</code> &nbsp;
  <code>Root Cause Debugging</code> &nbsp;
  <code>Context Compact</code>
</p>

> 如切如磋，如琢如磨 — 持续消除歧义，直到问题的形状足够准确。

Taku 是一组面向 Claude Code / coding agent 的 workflow skills，把真实工程任务拆成 Think → Plan → Build → Review → Verify → Reflect，并通过 `/taku-compact` 控制长任务上下文。

> **状态：** Beta workflow，已通过 9 个 eval scenarios + interactive dogfood 验证（5 PASS, 3 PARTIAL, 0 FAIL）。Taku 是带明确取向的 agentic coding 流程，适合结构化工程任务；宿主不支持 subagents 时保留 wave plan 但按顺序执行。

## 为什么需要 Taku

使用 coding agent 时最常见的失败：

- **Scope drift** — 需求在实现过程中悄悄膨胀
- **弱 review** — 代码"看起来没问题"，但 trust-boundary bug 和条件副作用被忽略
- **随机 patch** — AI 反复修改代码直到输出变化，然后宣布已解决
- **上下文丢失** — 长任务中 agent 忘记之前的决策和约束
- **长期记忆污染** — agent 频繁写入低质量"经验"，后续任务被噪声干扰

Taku 用结构化的六阶段 workflow 解决这些问题。

## 设计哲学

Taku 是面向 coding agent 的工程纪律 skill pack，不是通用 workflow
framework。它真正耐用的价值，是一组防止 agentic coding 失败的判断约束：
scope drift、事后合理化、缺少证据的完成声明，以及只修症状不找根因。

当前方向是 **principles over procedures**。各阶段 skill 保留自己需要的本地
流程，并在每个已安装 skill 内保留极简规则标签，让 Taku 随着模型能力提升
自然变轻，而不是变成更硬的流程笼子。

## 30 秒理解

```text
Request → Think → Plan → Build → Review → Verify → Reflect
                       (pass)         ↑       ↓
                       done           └── Debug ──┘ (fail)
```

典型流程：

1. `/taku-think` — 澄清需求，定义问题边界
2. `/taku-plan` — 生成带依赖图的可执行任务
3. `/taku-build` — 基于 TDD，以 sequential / parallel / hybrid 模式实现
4. `/taku-review` — 交付前审查真实 diff
5. **Verify** — 运行必要检查；失败时使用 `/taku-debug` 从根因开始调查
6. `/taku-reflect` — 仅在确实有值得保留的经验时执行沉淀

> **Verify 与 Debug：** Verification 是质量门禁。`/taku-debug` 是门禁失败或行为异常时使用的 skill。Taku 没有单独的 `/taku-test`。
>
> **Context Control：** 长任务、调试、审查、设计讨论或研究中，使用 `/taku-compact` 生成可恢复的工作 brief。它不是第七阶段，也不写长期 memory。

## 快速安装

```bash
# 全局安装所有 Taku 技能
npx skills add KKenny0/Taku -g --all

# 上游更新后
npx skills update -g
```

安装后开启新 session，输入 `/taku-` 确认命令已被发现：

```text
/taku-think  /taku-plan  /taku-build  /taku-review
/taku-debug  /taku-reflect  /taku-compact
```

建议安装后先运行 validator，确认 skill pack、slash command 和 eval scenarios 处于可用状态：

```bash
python3 scripts/validate_taku.py --install
```

加 `--strict` 可额外检查引用的外部脚本是否存在且可执行：`python3 scripts/validate_taku.py --strict`

也可以单独安装某个 skill：`npx skills add KKenny0/Taku -g --skill taku-think`

## 第一次运行

用一个小的 Quick-mode 任务试跑：

```text
/taku-think Add a --version flag to the existing CLI. It should print the package version and avoid changing other command behavior.
```

预期形态：

1. `/taku-think` 使用 Quick mode，给出 mini design
2. 你确认 mini design
3. `/taku-plan` 写紧凑计划，或任务足够小时轻量交接
4. `/taku-build` 基于 test anchor 实现，然后进入 review 和 verification

## 核心工作流

| 阶段 | 命令 | 使用时机 | 主要输出 |
|---|---|---|---|
| Think | `/taku-think` | 需求模糊或仍处于 idea 阶段 | 澄清后的 scope，`DESIGN.md` 中的设计决策 |
| Plan | `/taku-plan` | 设计已确认，需要可执行任务 | 基于 spec 的 `PLAN.md`，含 dependency graph |
| Build | `/taku-build` | `PLAN.md` 已准备好 | 已实现代码、测试、可见的构建进度 |
| Review | `/taku-review` | 交付前 | diff review 结论，scope drift 检查 |
| Debug | `/taku-debug` | 检查失败或行为异常 | 根因调查，定向修复 |
| Reflect | `/taku-reflect` | 某个模式或经验值得保留 | 经用户批准的 learnings，可选 retro report |

`/taku-think` 会根据任务复杂度自动选择 Quick、Design 或 Explore 模式——重要任务获得足够的流程，小任务避免过度仪式化。

### Bonus Utility Skills

| Skill | 命令 | 使用时机 | 主要输出 |
|---|---|---|---|
| Compact | `/taku-compact` | 长任务上下文膨胀、交接、恢复、调试、审查、设计或研究 | 带 source tags、unknowns、retrieval hints 和下一步的可恢复 brief |

`/taku-compact` 支持 `resume`、`handoff`、`debug`、`review`、`design` 和 `research` modes。它只整理当前任务上下文；长期经验通过 `/taku-reflect` 经用户批准后沉淀。

## Taku 的不同之处

### 1. 根据任务规模调整流程强度

`/taku-think` 自动选择流程强度：Quick（小改动）、Design（常规功能）、Explore（模糊 idea），避免一律采用重流程。

### 2. 把计划当作可执行工作

`/taku-plan` 不只是任务列表。它强制完成 scope review、architecture review、UI design review（仅在存在 UI 时），再生成带依赖标注、TDD anchors 和 execution hints 的 spec-based tasks。

Review 产物进入 `DESIGN.md`，`PLAN.md` 保持纯执行内容——goal、tasks、dependency graph。build agent 读取 plan 的 contract header 后，可以明确哪些是必须完成的内容，哪些是可选内容。

### 3. 显式化构建执行

`/taku-build` 负责执行方式决策，支持 Sequential（小任务或高度耦合）、Parallel（任务独立且宿主支持 subagents）和 Hybrid（wave 组织）三种形态。plan 已自检且仍在 approved scope 内时直接进入 BUILD。

### 4. 不把 review 简化成"看起来没问题"

`/taku-review` 读取真实 diff，检查 base branch drift，寻找测试经常覆盖不到的失败模式：不安全的 query construction、trust-boundary 错误、条件副作用、缺失的错误处理、scope drift。

### 5. 区分验证与调试

第五阶段是 verification gate，不是第二次 planning。检查失败时，`/taku-debug` 强调 evidence-first：investigate → pattern-match → rank hypotheses → verify root cause。这避免了常见的 AI bugfix 循环——反复修改代码直到输出变化，然后宣布解决。

### 6. 控制长期记忆写入

`/taku-reflect` 默认需要人工触发。只有经过用户批准的 patterns、pitfalls、preferences 和 discoveries 才会被保留。`.taku/learnings/*.jsonl` 是 canonical source，由 `skills/reflect/scripts/learnings.py` 管理。

### 7. 控制当前工作上下文

`/taku-compact` 扫描 durable sources、git evidence 和 session state，生成结构化 brief。Brief 明确标注哪些结论来自项目文件、git、当前对话，哪些只是推断；证据不足时必须写 `unknown`。

### 常见失败模式

| 常见失败 | Taku 的处理 |
|---|---|
| Scope 在实现中悄悄漂移 | `/taku-plan` 强制 scope review，build 时检查 drift |
| Review 流于形式，隐蔽 bug 被忽略 | `/taku-review` 读真实 diff，查 trust-boundary 等风险模式 |
| AI 反复乱 patch，不找根因 | `/taku-debug` 排序假设，验证根因后再修复 |
| 长任务上下文膨胀或丢失 | `/taku-compact` 写可恢复的 active-work brief |
| Agent 持续写入低质量"经验" | `/taku-reflect` 需人工触发，仅保留批准内容 |

## Before / After

**Without Taku:**

- 模糊 prompt → 快速代码生成
- 隐蔽的 scope drift
- 弱 review，甚至没有 review
- 验证断裂
- 随机式 debugging patch

**With Taku:**

- 被框定的请求 → 显式计划
- 可见的执行模式与 wave progress
- 交付前的 diff review
- 基于证据的 verification
- 根因导向的 debugging

## Case Studies

> 9 个 eval scenarios + interactive dogfood：5 PASS, 3 PARTIAL, 0 FAIL, 1 SKIP。Taku 的纪律机制在真实 eval 中阻止了哪些失败？三个具体案例：[查看 Case Studies](CASE_STUDIES.md)

## 使用场景

| 你的情况 | 建议入口 |
|---|---|
| 小改动，边界清楚 | `/taku-think` Quick mode → `/taku-build` |
| 需求模糊 | `/taku-think` |
| 已有明确 feature，需要拆任务 | `/taku-plan` |
| 已有 `PLAN.md` | `/taku-build` |
| 准备交付 | `/taku-review` |
| 测试失败或行为异常 | `/taku-debug` |
| 长任务要交接或恢复 | `/taku-compact` |
| 想沉淀经验或做回顾 | `/taku-reflect` |

## 安装详情

### 单独安装某个 skill

```bash
# 查看仓库中有哪些技能
npx skills add KKenny0/Taku -l

# 安装指定技能
npx skills add KKenny0/Taku -g --skill taku-think
```

| 参数 | 作用 |
|------|------|
| `-g` | 全局安装到 `~/.claude/skills/`（推荐）。不加则装到当前项目 `.claude/skills/` |
| `--all` | 安装仓库内全部技能 |
| `--skill <name>` | 指定安装某个技能，可重复使用 |
| `-l` | 仅列出可用技能，不安装 |

### 备选：git clone

```bash
git clone https://github.com/KKenny0/Taku.git ~/.claude/skills/taku
```

将每个 skill 暴露为独立 slash command：

```bash
# macOS / Linux
for skill in think plan build review debug reflect compact; do
  ln -s ~/.claude/skills/taku/skills/$skill ~/.claude/skills/taku-$skill
done
```

```powershell
# Windows PowerShell
foreach ($skill in @("think","plan","build","review","debug","reflect","compact")) {
  New-Item -ItemType Junction `
    -Path "$env:USERPROFILE\.claude\skills\taku-$skill" `
    -Target "$env:USERPROFILE\.claude\skills\taku\skills\$skill"
}
```

### 迁移说明

旧版仓库布局使用过 `skills/test/`，会导致 slash command 变成 `/taku-test`。当前布局使用 `skills/debug/`。如果安装过旧版本，请重新创建 symlink 或 junction 指向 `skills/debug/`，暴露 `/taku-debug`。

### OpenClaw

将同一个仓库作为 skill pack 使用，按照 `platform/openclaw.md` 中的 adapter notes 完成工具映射与能力检查。

## 仓库结构

```text
Taku/
├── README.md
├── logo.png
├── evals/
│   ├── README.md
│   └── real_task_scenarios.json
├── scripts/
│   └── validate_taku.py  # skill pack 自检脚本
├── skills/
│   ├── think/
│   ├── plan/
│   ├── build/
│   ├── review/
│   ├── debug/
│   ├── reflect/
│   └── compact/
├── platform/
│   └── openclaw.md
├── templates/
│   ├── design-doc.md
│   ├── plan.md
│   ├── compact-brief.md
│   └── retro-report.md
```

## 平台状态

| 平台 | 状态 | 说明 |
|---|---|---|
| Claude Code | 主要目标平台 | 使用 canonical `SKILL.md` 格式与 slash-command workflow |
| OpenClaw | 已包含 adapter | 工具映射记录在 `platform/openclaw.md` |

Taku 的方法可以跨平台使用。基于 subagents 的 parallelism 取决于宿主能力；没有该能力时，`/taku-build` 保留 wave visibility 并按顺序执行 wave tasks。

## 验证

发布变更前运行内置自检：

```bash
python3 scripts/validate_taku.py
```

默认 validator 也会检查 `evals/` 中的真实任务评估套件。这些场景是用来回归验证 routing 与 artifacts 的手动测试，不是 synthetic benchmark。修改阶段说明、安装行为或 README 主张时，应该使用这些场景做行为检查。

## 适合谁使用

Taku 适合那些已经意识到"原始代码生成"并不是主要瓶颈的团队或个人。

适合的场景：

- 希望 AI agent 在真实工程任务中更稳定、更可控
- 希望更好地控制 scope expansion
- 需要显式的 TDD 与 verification gates
- 希望拆分较大实现，同时不丢失 review discipline
- 希望在多个项目中复用同一套 engineering habits
- 希望长任务、调试、审查或研究中保留可恢复的上下文 brief

如果你只想"先快速写点东西，后面再说"，Taku 的流程可能偏重。它优化的是可靠性与杠杆率。

## FAQ

**每次都需要完整跑六个阶段吗？**

不需要。小而清晰的改动可能只需要 `/taku-think` 的 Quick mode 和 `/taku-build`。工作流会根据任务规模调整。

**Taku 能用于小任务吗？**

可以。`/taku-think` 的 Quick mode 足够轻量。只有任务确实需要时，才会进入更重的阶段。

**Taku 只适用于 Claude Code 吗？**

不是。仓库中包含 OpenClaw adapter。方法本身是平台无关的，差异主要体现在工具映射层。

**为什么没有 `/taku-test`？**

Verification 已作为工作流门禁存在。检查失败时，`/taku-debug` 负责根因调查。单独的 test skill 会模糊"运行检查"和"调查失败"之间的边界。

**每次改动都需要 `DESIGN.md` 和 `PLAN.md` 吗？**

不需要。它们会在 `/taku-think` 和 `/taku-plan` 判断任务需要时生成。Quick-mode 任务会跳过较重的文档产物。

## 灵感来源

Taku 建立在两个重要基础之上：

- **[Superpowers](https://github.com/obra/superpowers)** by [Jesse Vincent](https://github.com/obra)：engineering discipline、TDD enforcement、systematic debugging、evidence-based completion。
- **[gstack](https://github.com/garrytan/gstack)** by [Garry Tan](https://github.com/garrytan)：sprint thinking、product pressure-testing、QA methodology、parallel execution patterns。

Taku 是围绕六阶段 workflow 和可复用 agent habits 做出的更窄、更强调工程纪律的综合设计。

## Roadmap

- **Phase 1 — Prove It** ✅ 完成。9/10 eval scenarios + interactive dogfood 验证核心纪律机制有效。
- **Phase 2 — Harden** ✅ 完成。修复已识别 gap，编写 case studies，验证 debug Phase 2-3 interactive depth。
- **Phase 3 — Lean & Polish** 🔜 下一步。去重各 skill 共享的纪律原则，强化 principles over procedures，并保持 Taku 聚焦 coding-agent engineering discipline。

## License

MIT
