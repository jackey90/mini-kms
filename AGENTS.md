# AGENTS.md — IntelliKnow KMS AI 驱动开发指南

> 本文件是 AI 编码助手（Cursor）的项目总入口。所有 Agent 在启动前必须先读取本文件。

## 项目概述

**IntelliKnow KMS** — 企业级 Gen AI 知识管理系统

| 属性 | 值 |
|------|-----|
| 项目性质 | Tech Lead 面试项目（7天完成） |
| 核心需求文档 | `AD, Tech Lead, AKP.md` |
| 开发流程参考 | `software_rnd_full_process.md` |
| 技术栈 | Python (FastAPI) + SQLite/FAISS + React/Next.js |

**核心功能三件套**：
1. 多前端集成（Telegram + Teams/WhatsApp）
2. 文档驱动知识库（PDF/DOCX 自动解析）
3. 查询意图编排器（HR/Legal/Finance 分类路由）

详见 `AD, Tech Lead, AKP.md` 完整需求规格。

---

## Agent 索引

每个开发阶段对应一个 Agent 指令文件，位于 `.cursor/agents/`：

| Agent 文件 | 负责阶段 | 对应目录 | 分支前缀 |
|-----------|---------|---------|---------|
| `discovery-agent.md` | 市场与用户研究 | `discovery/` | `discovery/` |
| `prd-agent.md` | 产品定义（PRD） | `prd/` | `prd/` |
| `architecture-agent.md` | 方案与架构设计 | `architecture/` | `arch/` |
| `frontend-agent.md` | 前端研发 | `frontend/` | `frontend/` |
| `backend-agent.md` | 后端研发 | `backend/` | `backend/` |
| `qa-agent.md` | 测试与质量 | `qa/` | `qa/` |
| `release-agent.md` | 发布上线 | `release/` | `release/` |

**使用方式**：在 Cursor 中 @ 对应阶段目录，或直接在对话中说明当前处于哪个阶段，Agent 会自动读取对应的指令文件。

---

## Memory 系统

### 目的
记录每天与用户的讨论原始内容、决策结论和待确认问题，作为项目的"决策日志"。

### 目录
所有记录存放于 `memory/` 目录，按日期命名：`memory/YYYY-MM-DD.md`

### 文件格式

```markdown
# YYYY-MM-DD 项目讨论记录

## 讨论原始记录
（当日对话的关键内容摘录）

## 结论与决策
（已确认的技术/产品/架构决定，格式：✅ 决定内容）

## 待确认问题
（还未解决的疑问，格式：❓ 问题内容）

## 关联任务
（本日讨论影响到的 STATUS.md，格式：- phase/STATUS.md）
```

### Agent 更新 Memory 的规则
- 每次与用户确认了关键问题后，将结论写入当日 memory 文件的"结论与决策"
- 对话中出现的模糊需求，写入"待确认问题"
- 完成某阶段工作后，在对应 memory 文件的"关联任务"中记录

---

## STATUS.md 规范

每个阶段目录下有一个 `STATUS.md` 文件，记录该阶段的任务进度。

### 任务状态标记
| 标记 | 含义 |
|------|------|
| `[ ]` | 待开始 |
| `[~]` | 进行中 |
| `[x]` | 已完成 |
| `[?]` | 待确认（需要用户输入） |
| `[!]` | 阻塞（有依赖未解决） |

### Agent 更新 STATUS.md 的规则
1. 开始某个子任务前，将其标记为 `[~]`
2. 完成后改为 `[x]`，并在下方注记完成时间和关联 memory 链接
3. 遇到不清晰的地方，标记 `[?]` 并在 memory 当日文件中记录问题

---

## Git 分支与 Commit 规范

### 分支命名

```
<phase>/<short-description>
```

示例：
- `prd/functional-requirements`
- `arch/api-contract-design`
- `frontend/admin-dashboard`
- `backend/document-parser`
- `qa/integration-test`
- `release/v1.0.0`

### Commit Message 格式

```
[phase] 简短动作描述（动词开头）

Memory: memory/YYYY-MM-DD.md
```

示例：
```
[prd] 完成 FR-01 到 FR-06 功能需求初稿

Memory: memory/2026-02-21.md
```

```
[arch] 定义 REST API Contract 和数据模型

Memory: memory/2026-02-22.md
```

### 规则
- 每个阶段的工作在对应 branch 上进行，完成后 merge 到 `main`
- 每次 commit 必须带 `Memory:` 行，指向包含该工作决策背景的 memory 文件
- 不同阶段的变更不混在一个 commit 里

---

## Agent 通用工作规则

1. **读取上下文**：开始工作前先读取 `AD, Tech Lead, AKP.md`、当前阶段的 `STATUS.md`、以及最近的 `memory/` 文件
2. **遇到歧义必须确认**：需求不清晰时，先在 memory 文件中记录问题，然后向用户提问，不要自行假设
3. **更新进度**：完成每个子任务后立即更新 `STATUS.md`
4. **记录决策**：每次与用户确认了什么，都写入当日 memory 文件
5. **原子提交**：每个 commit 只包含一个逻辑变更单元
6. **不跨阶段**：不要在当前阶段的 commit 中混入其他阶段的内容
