# Backend 阶段状态

> 对应开发流程：Phase 5.2 后端研发（Backend）+ Phase 5.4 算法开发

**阶段目标**：实现 IntelliKnow KMS 核心后端服务，包括文档解析、向量检索、意图分类和前端集成。

**前置条件**：`architecture/STATUS.md` 中 LLD、API Contract 和数据模型已完成。

---

## 5.2.0 项目初始化

- [ ] Python 项目结构搭建（FastAPI）
- [ ] 依赖管理（`requirements.txt` / `pyproject.toml`）
- [ ] 环境变量配置（`.env.example`）
- [ ] SQLite 数据库初始化脚本

## 5.2.1 数据库层

- [ ] SQLite Schema 实现（文档表、意图空间表、查询日志表、集成配置表）
- [ ] ORM/查询封装（SQLAlchemy 或原生 SQLite）
- [ ] 数据库迁移脚本

## 5.2.2 文档管理模块

- [ ] 文件上传 API（`POST /api/documents`）
- [ ] PDF 解析（LangChain PDFLoader / pypdf）
- [ ] DOCX 解析（LangChain Docx2txtLoader）
- [ ] 文本分块策略（RecursiveCharacterTextSplitter）
- [ ] 向量化（OpenAI Embeddings 或 sentence-transformers）
- [ ] FAISS 索引构建与持久化
- [ ] 文档列表 API（`GET /api/documents`）
- [ ] 文档删除 API（`DELETE /api/documents/{id}`）
- [ ] 文档重新解析 API（`POST /api/documents/{id}/reparse`）

## 5.2.3 意图空间管理模块

- [ ] 意图空间 CRUD API（`/api/intents`）
- [ ] 默认意图空间初始化（HR / Legal / Finance）
- [ ] 意图空间与文档关联逻辑

## 5.2.4 查询编排器（Orchestrator）

- [ ] 查询入口 API（`POST /api/query`）
- [ ] 意图分类逻辑（LLM zero-shot 分类，置信度 ≥70%）
- [ ] 兜底路由（General 空间）
- [ ] RAG 检索（FAISS 向量检索 + 上下文窗口组装）
- [ ] LLM 响应生成（带引用的简洁回答）
- [ ] 响应格式适配（Telegram vs Teams 格式差异）

## 5.2.5 前端集成模块

- [ ] Telegram Bot 集成
  - [ ] Webhook 设置
  - [ ] 消息接收与回复
  - [ ] 连接测试 API
- [ ] 第二个集成（Teams or WhatsApp — 待 prd 阶段确认）
- [ ] 集成配置管理 API（`/api/integrations`）
- [ ] API Key 安全存储（环境变量 / 加密存储）

## 5.2.6 分析模块

- [ ] 查询日志记录（每次查询自动写入）
- [ ] 查询历史查询 API（`GET /api/analytics/queries`）
- [ ] KB 使用统计 API（`GET /api/analytics/kb-usage`）
- [ ] 数据导出 API（`GET /api/analytics/export`）

## 5.2.7 可观测性

- [ ] 请求日志中间件
- [ ] 错误日志（文档解析失败、LLM 调用失败）
- [ ] 健康检查端点（`GET /api/health`）

## 5.3 测试

- [ ] 单元测试（文档解析、意图分类逻辑）
- [ ] API 集成测试
- [ ] 向量检索准确性基础验证

---

## 阻塞项 / 待确认问题

> ❗ **[阻塞]** 等待 architecture 阶段确认 LLM 选型（OpenAI vs 本地）
> ❗ **[阻塞]** 等待 prd 阶段确认第二个前端集成（Teams vs WhatsApp）

---

## 完成记录

| 时间 | 完成事项 | Memory 链接 |
|------|---------|------------|
| 2026-02-21 | 后端阶段框架搭建 | [memory/2026-02-21.md](../memory/2026-02-21.md) |
