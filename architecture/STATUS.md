# Architecture 阶段状态

> 对应开发流程：Phase 3 方案与架构设计（Solution & Architecture）

**阶段目标**：确定技术选型、系统边界、API Contract 和数据模型，为开发阶段提供清晰蓝图。

**前置条件**：`prd/STATUS.md` 中所有 FR/NFR 完成，待确认问题已解答。

---

## 3.1 高层方案设计（HLD）

- [ ] 技术选型确认
  - [?] 前端框架：Streamlit（快速原型）vs Next.js（Admin UI 复杂度高）— **待确认**
  - [ ] 后端：FastAPI (Python)
  - [ ] 文档解析：LangChain Document Loaders
  - [ ] 向量存储：FAISS
  - [ ] 关系型存储：SQLite
  - [ ] 意图分类：OpenAI / 本地 LLM（zero-shot 分类）
- [ ] 系统边界与模块划分
- [ ] 关键链路设计（查询处理完整流程）
- [ ] 风险与回滚策略
- 产出：`architecture/HLD.md`

## 3.2 详细设计（LLD）

- [ ] 模块划分（`backend/` 下的包结构）
- [ ] REST API Contract 定义
  - [ ] 文档管理 API（上传/列表/删除/重解析）
  - [ ] 意图空间管理 API（CRUD）
  - [ ] 查询 API（提交查询 → 返回分类 + 响应）
  - [ ] 分析 API（查询历史、KB 使用统计）
  - [ ] 前端集成管理 API（配置 / 测试连接）
- [ ] 数据模型 / ERD（SQLite Schema）
- [ ] 异常处理与降级策略
- 产出：`architecture/LLD.md`、`architecture/api-contract.md`、`architecture/data-model.md`

## 3.3 UX/UI 设计

- [ ] 信息架构（页面层级、导航结构）
- [ ] 关键页面交互稿（文本描述 / 线框图）
  - [ ] Admin Dashboard
  - [ ] KB Management
  - [ ] Intent Configuration
  - [ ] Frontend Integration
  - [ ] Analytics
- 产出：`architecture/ui-wireframes.md`

## 3.4 算法系统架构

- [ ] 文档解析流水线（PDF/DOCX → Chunks → Embeddings → FAISS）
- [ ] 向量检索策略（相似度阈值、Top-K）
- [ ] 意图分类方案（Prompt 设计 + 置信度计算）
- [ ] RAG 响应生成链路
- 产出：`architecture/algorithm-arch.md`

---

## 阻塞项 / 待确认问题

> ❓ **[待确认]** 前端框架选 Streamlit 还是 Next.js？
> - Streamlit：Python-native，快速，但 UI 灵活性低
> - Next.js：更好的 Admin UI，但需要前后端分离
> （7天时限下，建议优先选 Next.js + FastAPI，因为 UI 有5个复杂页面）

> ❓ **[待确认]** LLM 选型：OpenAI API 还是本地 LLM（Ollama 等）？影响部署复杂度。

---

## 完成记录

| 时间 | 完成事项 | Memory 链接 |
|------|---------|------------|
| 2026-02-21 | 架构阶段框架搭建 | [memory/2026-02-21.md](../memory/2026-02-21.md) |
