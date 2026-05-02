<p align="center">
  <img src="logo.png" alt="Taku 琢" width="180" />
</p>

<h1 align="center">Taku 琢</h1>

<p align="center"><strong>一个面向 AI 辅助软件交付的纪律化 Sprint 系统。</strong></p>

<p align="center">
  <a href="README.en.md">English README</a>
</p>

<p align="center">
  清晰思考，具体计划，以 TDD 构建，审查真实 diff，定位根因，沉淀关键经验。
</p>

<p align="center">
  Taku 通过一套结构化的六阶段 Sprint，帮助 coding agent 更稳定地交付可靠软件：
  澄清问题，生成可执行计划，以可见结构完成构建，审查真实代码变更，基于证据完成验证，并在检查失败时从根因开始调试。
</p>

> 如切如磋，如琢如磨
>
> Taku 意为“雕琢、打磨玉石”。重点不在于生成更多内容，重点在于持续消除歧义，直到问题的形状足够准确。

> **状态：** Beta workflow。Taku 是一套带明确取向的 agentic coding 流程，适合结构化工程任务；不同宿主能力不同。宿主不支持 subagents 时，Taku 会保留 wave plan，但按顺序在本地执行这些 waves。

## 目录

- [快速开始](#快速开始)
- [核心工作流](#核心工作流)
- [Taku 的不同之处](#taku-的不同之处)
- [Before / After](#before--after)
- [安装](#安装)
- [仓库结构](#仓库结构)
- [平台状态](#平台状态)
- [验证](#验证)
- [适合谁使用](#适合谁使用)
- [FAQ](#faq)
- [灵感来源](#灵感来源)
- [Roadmap 方向](#roadmap-方向)
- [License](#license)

## 快速开始

```text
Request → Think → Plan → Build → Review → Verify → Reflect
                       (pass)         ↑       ↓
                       done           └── Debug ──┘ (fail)
```

一个真实任务的典型流程如下：

1. `/taku-think`：澄清需求，定义问题边界。
2. `/taku-plan`：生成带依赖图的可执行任务。
3. `/taku-build`：基于 TDD，以 sequential / parallel / hybrid 模式实现。
4. `/taku-review`：在交付前审查真实 diff。
5. Verify：运行必要检查。如果失败，使用 `/taku-debug` 从根因开始调查。
6. `/taku-reflect`：仅在确实有值得保留的经验时执行沉淀。

> **Verify 与 Debug：** Verification 是工作流中的质量门禁。`/taku-debug` 是当门禁失败，或者行为已经异常时使用的 skill。Taku 没有单独的 `/taku-test`。

### 示例 Sprint

**任务：** 增加 retry-safe 的 webhook delivery tracking。

- **Think**：澄清幂等边界，定义失败模式，识别必要的可观测性。
- **Plan**：新增 delivery status model，持久化 attempt metadata，定义 retry policy，添加集成测试。
- **Build**：实现存储变更，添加 retry coordinator，补齐测试。
- **Review**：审查 diff 中潜在的状态迁移 bug，确认没有 scope drift。
- **Verify / Debug**：运行测试，复现失败路径，在 patch 前确认真实根因。

## 核心工作流

Taku 围绕六个聚焦的阶段 skill 组织：

| 阶段 | 命令 | 使用时机 | 主要输出 |
|---|---|---|---|
| Think | `/taku-think` | 需求模糊，或者仍处于 idea 阶段 | 澄清后的 scope，记录在 `DESIGN.md` 中的设计决策 |
| Plan | `/taku-plan` | 设计已确认，需要可执行任务 | 基于 spec 的 `PLAN.md`，包含 dependency graph |
| Build | `/taku-build` | `PLAN.md` 已准备好 | 已实现代码、测试、可见的构建进度 |
| Review | `/taku-review` | 交付前 | diff review 结论，scope drift 检查 |
| Debug | `/taku-debug` | 检查失败或行为异常 | 根因调查，定向修复 |
| Reflect | `/taku-reflect` | 某个模式或经验值得保留 | 经用户批准的 learnings，可选 retro report |

这些 skills 被设计为可以在阶段之间交接工作。`/taku-think` 会根据任务复杂度自动选择 Quick、Design 或 Explore 模式。重要任务会获得足够严格的流程，小任务则避免过度仪式化。

## Taku 的不同之处

### 1. 根据任务规模调整流程强度

`/taku-think` 不会一律采用重流程。它会自动选择：

- **Quick**：适用于边界清晰的小改动。
- **Design**：适用于常规功能开发。
- **Explore**：适用于仍然过于模糊、尚不能直接实现的 idea-stage 请求。

### 2. 把计划当作可执行工作

`/taku-plan` 不只是写任务列表。它会强制完成：

- 实现前的 scope review。
- 架构扩散前的 architecture review。
- 仅在确实存在 UI 时执行 UI design review。
- 带依赖标注和 TDD anchors 的 spec-based tasks。
- 给 build agent 使用的执行提示，包括 execution mode 和 wave grouping。

Review 产物，例如 scope assessment、architecture diagrams、edge cases，会进入 `DESIGN.md`。`PLAN.md` 保持为纯执行内容，包括 goal、tasks、dependency graph。build agent 读取 plan 的 contract header 后，可以明确哪些是必须完成的内容，哪些是可选内容。

### 3. 显式化构建执行

`/taku-build` 负责执行方式决策。在 plan 已自检且仍处于已批准 scope 内时，它会直接进入 BUILD。

它支持三种执行形态：

- **Sequential**：适用于小任务或高度耦合的任务。
- **Parallel**：适用于任务彼此独立且宿主支持 subagents 的场景；不支持时按 wave 顺序执行。
- **Hybrid**：适用于按 wave 组织的执行。wave 之间顺序执行，同一个 wave 内的任务在宿主支持时可并行执行。

### 4. 不把 review 简化成“看起来没问题”

`/taku-review` 会读取真实 diff，检查 base branch drift，并寻找测试经常覆盖不到的失败模式：

- 不安全的 query construction。
- LLM 使用中的 trust-boundary 错误。
- 条件副作用。
- 缺失的错误处理。
- 需求意图与实际交付之间的 scope drift。

### 5. 区分验证与调试

第五阶段是 verification gate。它不是第二次 planning，也不是模糊的”做一下 QA”。运行必要检查后，`/taku-debug` 用于检查失败或行为已经异常的分支。

Taku 的 debug flow 强调 evidence-first：

1. investigate
2. pattern-match
3. rank hypotheses
4. verify the actual root cause

这样可以避免常见的 AI bugfix 循环：不断修改代码，直到输出发生变化，然后把它当作已经解决。

### 6. 控制长期记忆写入

`/taku-reflect` 默认需要人工触发。Taku 不会因为发生过一次事情就持续写入“learnings”。

在某个项目第一次成功运行 reflect 后，它可以建议把一个简短的 learnings-discovery note 写入 `AGENTS.md` 或 `CLAUDE.md`。这个 note 只是可选发现层，不是事实源；`.taku/learnings/*.jsonl` 才是 canonical source，并由 `skills/reflect/scripts/learnings.py` 管理。

只有经过用户批准的 patterns、pitfalls、preferences 和 discoveries 才会被保留。

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

## 安装

### Claude Code

使用 [skills CLI](https://github.com/anthropics/skills) 一行安装（推荐）：

```bash
# 全局安装所有 Taku 技能
npx skills add KKenny0/Taku -g --all
```

也可以单独安装某个阶段：

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

上游更新后执行：

```bash
npx skills update -g
```

安装完成后，开启一个新 session 并输入 `/taku-`，确认六个阶段命令已被发现：

```text
/taku-think
/taku-plan
/taku-build
/taku-review
/taku-debug
/taku-reflect
```

### 备选：git clone

如果希望手动安装：

```bash
git clone https://github.com/KKenny0/Taku.git ~/.claude/skills/taku
```

将每个阶段暴露为独立 slash command：

```bash
# macOS / Linux
for phase in think plan build review debug reflect; do
  ln -s ~/.claude/skills/taku/skills/$phase ~/.claude/skills/taku-$phase
done
```

```powershell
# Windows PowerShell
foreach ($phase in @("think","plan","build","review","debug","reflect")) {
  New-Item -ItemType Junction `
    -Path "$env:USERPROFILE\.claude\skills\taku-$phase" `
    -Target "$env:USERPROFILE\.claude\skills\taku\skills\$phase"
}
```

克隆后也可以运行安装验证脚本：

```bash
python3 scripts/validate_taku.py --install
```

### 第一次运行

安装完成后，建议先用一个小的 Quick-mode 任务试运行：

```text
/taku-think Add a --version flag to the existing CLI. It should print the package version and avoid changing other command behavior.
```

预期的第一次运行形态：

1. `/taku-think` 使用 Quick mode，并给出 mini design。
2. 你确认 mini design。
3. `/taku-plan` 写一个紧凑计划，或在任务足够小时使用轻量计划交接。
4. `/taku-build` 基于 test anchor 实现，然后进入 review 和 verification。

更大的任务可以从以下入口开始：

- 对于模糊需求，使用 `/taku-think`。
- 对于已经明确 scope、需要拆成可执行任务的功能，使用 `/taku-plan`。
- 只有当 `PLAN.md` 已准备好时，才使用 `/taku-build`。

### 迁移说明

旧版仓库布局使用过 `skills/test/`，这会带来两个问题：

- 安装后的 slash command 可能变成 `/taku-test`，即使实际 skill 名称是 `taku-debug`。
- verification 与 debugging 的阶段语义容易被混在一起。

当前布局使用 `skills/debug/`。如果你安装过旧版本，请重新创建 symlink 或 junction，使其指向 `skills/debug/`，并暴露 `/taku-debug`。

### OpenClaw

将同一个仓库作为 skill pack 使用，然后按照 `platform/openclaw.md` 中的 adapter notes 完成工具映射与能力检查。

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
│   └── reflect/
├── platform/
│   └── openclaw.md
├── templates/
│   ├── design-doc.md
│   ├── plan.md
│   └── retro-report.md
```

## 平台状态

| 平台 | 状态 | 说明 |
|---|---|---|
| Claude Code | 主要目标平台 | 使用 canonical `SKILL.md` 格式与 slash-command workflow |
| OpenClaw | 已包含 adapter | 工具映射记录在 `platform/openclaw.md` |

Taku 的方法可以跨平台使用，具体工具细节由平台适配层处理。基于 subagents 的 parallelism 取决于宿主能力；没有该能力时，`/taku-build` 会保留 wave visibility，并在本地按顺序执行 wave tasks。

## 验证

发布变更前运行内置自检：

```bash
python3 scripts/validate_taku.py
```

克隆或重建命令链接后，运行安装检查：

```bash
python3 scripts/validate_taku.py --install
```

默认 validator 也会检查 `evals/` 中的真实任务评估套件。这些场景是用来回归验证 routing 与 artifacts 的手动测试，不是 synthetic benchmark。修改阶段说明、安装行为或 README 主张时，应该使用这些场景做行为检查。

## 适合谁使用

Taku 适合那些已经意识到“原始代码生成”并不是主要瓶颈的团队或个人。

它尤其适合以下场景：

- 希望 AI agent 在真实工程任务中表现得更稳定、更可控。
- 希望更好地控制 scope expansion。
- 需要显式的 TDD 与 verification gates。
- 希望拆分较大实现，同时不丢失 review discipline。
- 希望在多个项目中复用同一套 sprint shape。

如果你只想“先快速写点东西，后面再说”，Taku 的流程可能显得偏重。它的优化目标是可靠性与杠杆率。

## FAQ

**每次都需要完整跑六个阶段吗？**

不需要。小而清晰的改动可能只需要 `/taku-think` 的 Quick mode 和 `/taku-build`。工作流会根据任务规模调整。

**Taku 能用于小任务吗？**

可以。`/taku-think` 的 Quick mode 足够轻量。只有任务确实需要时，才会进入更重的阶段。

**Taku 只适用于 Claude Code 吗？**

不是。仓库中包含 OpenClaw adapter。方法本身是平台无关的，差异主要体现在工具映射层。

**为什么没有 `/taku-test`？**

Verification 已作为工作流门禁存在。检查失败时，`/taku-debug` 负责根因调查。单独的 test skill 会模糊“运行检查”和“调查失败”之间的边界。

**每次改动都需要 `DESIGN.md` 和 `PLAN.md` 吗？**

不需要。它们会在 `/taku-think` 和 `/taku-plan` 判断任务需要时生成。Quick-mode 任务会跳过较重的文档产物。

## 灵感来源

Taku 建立在两个重要基础之上：

- **[Superpowers](https://github.com/obra/superpowers)** by [Jesse Vincent](https://github.com/obra)：engineering discipline、TDD enforcement、systematic debugging、evidence-based completion。
- **[gstack](https://github.com/garrytan/gstack)** by [Garry Tan](https://github.com/garrytan)：sprint thinking、product pressure-testing、QA methodology、parallel execution patterns。

Taku 是围绕六阶段 sprint 做出的更窄、更强调工程纪律的综合设计。

## Roadmap 方向

当前仓库已经具备核心 sprint spine。下一层重点不应只是增加更多 commands，而应继续提高执行质量：

- 更严格的 phase handoff contracts。
- 更显式的 BUILD scheduling 和长任务中的 wave visibility。
- 对真实 repo 变更更强的 review / test coverage。
- 更好的 packaging 与 distribution ergonomics。
- 更清晰的 active product work 使用示例。

## License

MIT
