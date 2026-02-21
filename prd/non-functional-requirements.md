# IntelliKnow KMS — 非功能需求（Non-Functional Requirements）

---

## NFR-01 性能（Performance）

| ID | 需求 | 指标 | 优先级 |
|----|------|------|--------|
| NFR-01-1 | Bot 端到端响应时延 | ≤ 3 秒（从用户发送消息到 Bot 回复，含意图分类 + 检索 + LLM 生成） | P0 |
| NFR-01-2 | Admin UI 页面加载时间 | ≤ 2 秒（首屏，本地网络） | P1 |
| NFR-01-3 | 文档解析时间 | ≤ 60 秒（单个 ≤ 10MB 的 PDF/DOCX） | P1 |
| NFR-01-4 | FAISS 向量检索时延 | ≤ 500ms（知识库 ≤ 100 文档时） | P0 |

**说明**：NFR-01-1 是最关键约束，直接影响用户体验。LLM 调用（gpt-3.5-turbo）通常 1-2 秒，FAISS 检索 < 100ms，整体可满足 3 秒要求。

---

## NFR-02 并发与可用性（Concurrency & Availability）

| ID | 需求 | 指标 | 优先级 |
|----|------|------|--------|
| NFR-02-1 | 并发查询支持 | MVP 阶段：≥ 5 个并发查询不出错 | P1 |
| NFR-02-2 | 服务启动时间 | `docker-compose up` 后 30 秒内所有服务就绪 | P1 |
| NFR-02-3 | 本地运行稳定性 | Demo 期间（1小时）不崩溃 | P0 |

**说明**：MVP 为单机本地部署，不要求高可用（HA），不需要负载均衡。

---

## NFR-03 安全性（Security）

| ID | 需求 | 说明 | 优先级 |
|----|------|------|--------|
| NFR-03-1 | API Key 不明文存储 | Telegram Token / Teams App Password / OpenAI API Key 全部通过环境变量（`.env`）管理，代码中不出现明文 | P0 |
| NFR-03-2 | .env 不提交 Git | `.gitignore` 必须包含 `.env`；提供 `.env.example` 模板 | P0 |
| NFR-03-3 | Admin UI 无认证（MVP） | MVP 阶段无登录功能，假设本地内网使用；README 中注明此限制 | P0（接受此风险） |
| NFR-03-4 | 文件类型校验 | 上传文件仅允许 `.pdf` 和 `.docx`，后端双重校验（MIME type + 扩展名） | P0 |
| NFR-03-5 | 文件大小限制 | 单文件 ≤ 50MB，防止资源耗尽 | P1 |

---

## NFR-04 可部署性（Deployability）

| ID | 需求 | 说明 | 优先级 |
|----|------|------|--------|
| NFR-04-1 | Docker Compose 一键启动 | `docker-compose up` 启动全部服务（FastAPI 后端 + Next.js 前端） | P0 |
| NFR-04-2 | 零外部服务依赖 | 除 OpenAI API 外，所有存储（SQLite/FAISS）本地运行，无需安装 Redis/PostgreSQL 等 | P0 |
| NFR-04-3 | 数据持久化 | 数据库文件和 FAISS 索引通过 Docker Volume 持久化，容器重启不丢数据 | P0 |
| NFR-04-4 | 跨平台支持 | Docker Compose 在 macOS / Linux / Windows（WSL2）均可运行 | P1 |
| NFR-04-5 | 干净环境可复现 | README Quick Start 步骤在全新环境（仅安装 Docker + API Keys）可成功启动 | P0 |

---

## NFR-05 可观测性（Observability）

| ID | 需求 | 说明 | 优先级 |
|----|------|------|--------|
| NFR-05-1 | 请求日志 | FastAPI 记录所有 API 请求（时间 / 路径 / 状态码 / 耗时），输出到 stdout | P1 |
| NFR-05-2 | 错误日志 | 文档解析失败、LLM 调用失败的错误信息写入日志 | P0 |
| NFR-05-3 | 健康检查端点 | `GET /api/health` 返回服务状态 | P1 |
| NFR-05-4 | 文档处理状态追踪 | Admin UI 可见文档的处理状态（Pending / Processing / Processed / Error） | P0 |

---

## NFR-06 可维护性（Maintainability）

| ID | 需求 | 说明 | 优先级 |
|----|------|------|--------|
| NFR-06-1 | 代码语言规范 | 所有代码和注释使用英文 | P0 |
| NFR-06-2 | README 完整性 | 包含：项目描述、技术栈、本地启动步骤（≤10步）、集成配置指南 | P0 |
| NFR-06-3 | .env.example 完整 | 每个环境变量有注释说明其用途和获取方式 | P0 |
| NFR-06-4 | API 文档 | FastAPI 自动生成 OpenAPI 文档（`/docs`），无需额外维护 | P1 |

---

## 约束汇总

| 约束类型 | 内容 |
|---------|------|
| 时间约束 | 7个日历日完成 MVP |
| 技术约束 | 仅使用轻量化技术栈（SQLite/FAISS），禁止复杂云服务 |
| 部署约束 | 本地 Docker Compose，无云端部署 |
| 预算约束 | 仅 OpenAI API 费用（预计 Demo 阶段 < $5） |
| 人员约束 | Solo 开发，无外部协作 |
