# IntelliKnow KMS — MVP 范围与里程碑

## 1. MVP 目标

在 **7个日历日** 内交付一个可演示的 IntelliKnow KMS，满足以下核心目标：
- 通过 Telegram + Teams 两个渠道接收并回答企业知识查询
- 支持 PDF / DOCX 文档自动解析并构建可检索知识库
- 通过意图分类路由到 HR / Legal / Finance 三个知识域
- Admin 可通过 Web 界面管理文档、意图空间和查看分析数据

---

## 2. MVP 功能边界（In Scope）

### P0 — 必须交付（核心演示路径）

| 功能 | 说明 |
|------|------|
| Telegram Bot 消息收发 | Bot Token 配置、接收消息、返回 RAG 响应 |
| PDF / DOCX 文档上传与解析 | Admin UI 上传 → LangChain 解析 → FAISS 向量化 → 可查询 |
| 意图分类路由 | 3个默认空间（HR / Legal / Finance）+ General 兜底 |
| RAG 检索响应 | 语义检索 + LLM 生成带来源引用的回答 |
| Admin KB Management 页面 | 文档列表、上传、删除、状态查看 |
| Admin Intent Configuration 页面 | 意图空间 CRUD + 查询分类日志 |

### P1 — 应该交付（完整演示）

| 功能 | 说明 |
|------|------|
| Microsoft Teams Bot | Bot Framework 集成，消息收发 |
| Admin Dashboard 主页 | 4个模块状态卡片 |
| Admin Frontend Integration 页面 | 连接状态 + 测试按钮 |
| Admin Analytics 页面 | 查询历史表格 + KB 使用统计 |
| 数据导出 | CSV 导出查询日志 |

### P2 — 可选（时间允许）

| 功能 | 说明 |
|------|------|
| 文档重新解析 | 更新文档内容后触发重新向量化 |
| 移动端响应式 Admin UI | 桌面优先，移动端可选 |
| 意图分类置信度可配置 | Admin 界面调整阈值（默认 70% 已足够） |

---

## 3. Non-Goals（MVP 不做）

| 不做 | 原因 |
|------|------|
| 用户认证 / 权限管理 | MVP 单用户场景，时间有限 |
| 多租户 / 多企业支持 | 超出 7 天范围 |
| 云端部署 | 本地 Docker Compose 已满足演示要求 |
| 第三方 SSO（LDAP / SAML） | 超出 MVP 范围 |
| 实时流式响应（Streaming） | Polling 模式已满足 ≤3s 要求 |
| 文档版本管理 | 仅支持覆盖更新 |
| 移动端原生 App | Web Admin UI 已满足 |
| Slack / WhatsApp 集成 | MVP 仅做 Telegram + Teams |
| 模型微调 / 自定义 Embedding | 使用 OpenAI API 已满足准确率要求 |

---

## 4. Day 1-7 里程碑计划

| 日期 | 里程碑 | 主要任务 | 交付物 |
|------|--------|---------|--------|
| **Day 1** | 架构 + 项目骨架 | 架构设计（HLD/LLD/API Contract/DB Schema）；后端 FastAPI 初始化；前端 Next.js 初始化；Docker Compose 骨架 | `architecture/` 文档；可运行的空项目 |
| **Day 2** | 文档解析 Pipeline | PDF/DOCX 上传 API；LangChain 解析；FAISS 向量化；文档管理 CRUD API | `POST /documents` 可用；文档可被检索 |
| **Day 3** | 意图分类 + RAG | OpenAI zero-shot 意图分类；FAISS 语义检索；LLM 响应生成；查询 API | `POST /query` 端到端可用 |
| **Day 4** | Telegram Bot | Telegram Bot Polling 模式；消息路由到查询 API；回复格式适配 | Telegram Bot 可接收问题并回答 |
| **Day 5** | Admin UI 核心页面 | Next.js KB Management 页面；Intent Configuration 页面；API 对接 | Admin 可上传文档、管理意图空间 |
| **Day 6** | Teams Bot + Analytics | Teams Bot Framework 集成；Analytics 页面；Dashboard；Frontend Integration 页面 | 双 Bot 均可用；Admin 界面完整 |
| **Day 7** | 集成测试 + 交付 | 端到端联调；README 文档；AI-USAGE.md；Demo 录制/验证；Docker Compose 完整测试 | 完整可演示的系统 |

### 关键路径

```
DB Schema → 文档解析 → RAG 检索 → 查询 API → Telegram Bot（P0 核心路径）
                                              ↘ Teams Bot（P1）
                                 ↗ Admin UI（并行开发，Day 5）
```

---

## 5. 依赖与风险

| 依赖/风险 | 描述 | 缓解措施 |
|-----------|------|---------|
| OpenAI API Key | 需要有效的 OpenAI API Key | 提前准备，.env 配置 |
| Teams Bot 注册复杂度 | Azure Bot 注册流程可能耗时 | Day 1 即评估，若超过半天改为 Mock |
| Telegram Polling 模式 | 本地 Demo 无需 Webhook，Polling 更简单 | 默认使用 Polling |
| LLM 分类准确率 | zero-shot 可能低于 70% | Day 3 验证，不达标则增加意图关键词提示 |
