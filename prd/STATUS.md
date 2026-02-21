# PRD 阶段状态

> 对应开发流程：Phase 2 产品定义（Product Definition）

**阶段目标**：将需求文档转化为可执行的 PRD（功能需求 + 非功能需求 + 验收标准）。

---

## 2.1 范围与边界（Scope）

- [x] MVP 功能边界确认（P0/P1/P2 三级）
- [x] Non-goals 明确（14项不做的功能）
- [x] 里程碑拆解（Day 1-7 的交付计划 + 关键路径）
- 产出：[`prd/scope.md`](scope.md) ✅

## 2.2 功能需求（Functional Requirements）

### FR-01 多前端集成
- [x] FR-01-1: Telegram Bot 集成（P0）— Polling 模式，/start 命令，响应格式
- [x] FR-01-2: Microsoft Teams Bot 集成（P1）— Bot Framework SDK
- [x] FR-01-3: 连接状态监控（P1）— Connected/Disconnected/Error + 末4位显示
- [x] FR-01-4: 端到端测试功能（P1）— Test 按钮 + 响应时间显示

### FR-02 文档驱动知识库
- [x] FR-02-1: PDF 文档上传与解析（P0）— PyPDFLoader + chunk_size=500
- [x] FR-02-2: DOCX 文档上传与解析（P0）— Docx2txtLoader
- [x] FR-02-3: 意图空间关联（P0）— 上传时指定，FAISS 分区索引
- [x] FR-02-4: 文档删除（P1）
- [x] FR-02-5: 文档重新解析（P2）
- [x] FR-02-6: 基础错误处理（P0）— 格式校验 + Error 状态
- [x] FR-02-7: 文档搜索与过滤（P1）

### FR-03 意图空间编排器
- [x] FR-03-1: 默认意图空间（P0）— HR / Legal / Finance + 各自描述和关键词
- [x] FR-03-2: 自定义意图空间 CRUD（P1）
- [x] FR-03-3: AI 意图分类（P0）— gpt-3.5-turbo zero-shot，置信度 ≥ 0.7
- [x] FR-03-4: 兜底路由（P0）— General 空间 + 明确提示
- [x] FR-03-5: 意图路由后 RAG 检索（P0）— FAISS Top-5

### FR-04 知识检索与响应
- [x] FR-04-1: 带引用的 RAG 响应（P0）— ≤200字 + 来源文档名
- [x] FR-04-2: 多前端响应格式适配（P1）— Telegram emoji / Teams Adaptive Card
- [x] FR-04-3: 无匹配时的兜底响应（P0）— 两种情况（空 KB / 低相关性）

### FR-05 Admin UI
- [x] FR-05-1: Dashboard 主页（P1）— 4个模块卡片 + 关键统计
- [x] FR-05-2: Frontend Integration 页面（P1）— 状态卡片 + 配置 + Test
- [x] FR-05-3: KB Management 页面（P0）— 文档列表 + 上传区 + 搜索过滤
- [x] FR-05-4: Intent Configuration 页面（P0）— 意图卡片 + 分类日志 + 编辑表单
- [x] FR-05-5: Analytics 页面（P1）— 历史表格 + KB 统计 + 导出

### FR-06 分析与历史
- [x] FR-06-1: 查询日志自动记录（P0）— 7个字段完整定义
- [x] FR-06-2: KB 使用情况追踪（P1）— access_count 计数器
- [x] FR-06-3: 数据导出（P2）— CSV 格式

- 产出：[`prd/functional-requirements.md`](functional-requirements.md) ✅

## 2.3 非功能需求（Non-Functional Requirements）

- [x] NFR-01: 性能（Bot ≤3s / 页面 ≤2s / 解析 ≤60s / FAISS ≤500ms）
- [x] NFR-02: 并发（≥5并发 / 启动 ≤30s）
- [x] NFR-03: 安全（API Key 环境变量 / .env gitignore / 文件类型校验）
- [x] NFR-04: 可部署性（Docker Compose / 零外部服务 / 数据持久化）
- [x] NFR-05: 可观测性（请求日志 / 错误日志 / 健康检查）
- [x] NFR-06: 可维护性（英文代码 / README / .env.example）

- 产出：[`prd/non-functional-requirements.md`](non-functional-requirements.md) ✅

## 2.4 验收标准

- [x] AC-FR01: 多前端集成验收标准（5条，P0~P1）
- [x] AC-FR02: 文档知识库验收标准（6条，P0~P1）
- [x] AC-FR03: 意图编排器验收标准（5条，P0~P1）
- [x] AC-FR04: 知识检索响应验收标准（4条，P0~P1）
- [x] AC-FR05: Admin UI 验收标准（4条，P0~P1）
- [x] AC-FR06: 分析历史验收标准（2条，P0~P2）
- [x] AC-NFR: 非功能验收标准（5条，P0~P1）

- 产出：[`prd/acceptance-criteria.md`](acceptance-criteria.md) ✅（英文）

---

## 阻塞项 / 待确认问题

> 无阻塞项 — PRD 阶段全部完成，可进入架构设计阶段。

---

## 完成记录

| 时间 | 完成事项 | Memory 链接 |
|------|---------|------------|
| 2026-02-21 | PRD 框架搭建，基于需求文档提取功能列表 | [memory/2026-02-21.md](../memory/2026-02-21.md) |
| 2026-02-21 | 完成 scope.md（MVP 范围 + Non-goals + Day 1-7 里程碑） | [memory/2026-02-21.md](../memory/2026-02-21.md) |
| 2026-02-21 | 完成 functional-requirements.md（FR-01 ~ FR-06，含用户故事） | [memory/2026-02-21.md](../memory/2026-02-21.md) |
| 2026-02-21 | 完成 non-functional-requirements.md（NFR-01 ~ NFR-06） | [memory/2026-02-21.md](../memory/2026-02-21.md) |
| 2026-02-21 | 完成 acceptance-criteria.md（30条 Given/When/Then，英文） | [memory/2026-02-21.md](../memory/2026-02-21.md) |
