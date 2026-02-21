# Release 阶段状态

> 对应开发流程：Phase 7 发布上线（Release & Launch）+ Phase 3.3 交付要求

**阶段目标**：完成 GitHub 仓库发布、Demo 部署、README 文档，满足面试交付要求。

**前置条件**：`qa/STATUS.md` 中 UAT 全部通过。

---

## 7.1 发布准备

- [ ] 版本号确定（v1.0.0 MVP）
- [ ] 代码清理（移除调试代码、注释敏感信息）
- [ ] 依赖版本锁定（`requirements.txt` 固定版本）
- [ ] 环境变量文档化（`.env.example` 完整）
- [ ] 回滚方案（本地 demo：回滚到上一个 git tag）

## 7.2 GitHub 仓库准备

- [ ] 仓库设为 Public
- [ ] README.md 完整性检查
  - [ ] 项目描述（What & Why）
  - [ ] 技术栈说明
  - [ ] 本地启动步骤（Step-by-step）
  - [ ] 前端集成配置指南（Telegram / Teams 配置步骤）
  - [ ] API 文档索引（链接到 `architecture/api-contract.md`）
  - [ ] AI 使用反思（`AI-USAGE.md` 或 README 章节）
- [ ] 示例数据准备（2份示例文档：1个 PDF + 1个 DOCX）
- [ ] `.gitignore` 确认（`.env`、`*.db`、`faiss_index/` 不提交）

## 7.3 Demo 部署

- [x] 部署方式确认：**本地 Demo + Docker Compose**
- [ ] `docker-compose.yml`（一键启动 FastAPI + Next.js + 数据卷）
- [ ] 本地启动文档（README 中的 Quick Start）

## 7.4 AI 使用反思文档（需求明确要求）

- [ ] `AI-USAGE.md` 创建
  - [ ] 场景1：文档解析中 AI 的使用（PDF 表格提取案例）
  - [ ] 场景2：前端集成中 AI 的使用（响应格式适配案例）
  - [ ] AI 使用的策略意图（而非工具名称）
  - [ ] AI 输出的调整与优化

## 7.5 上线验证

- [ ] 完整 Demo 流程演练（从上传文档 → Telegram 提问 → 获得答案）
- [ ] 已知问题清单记录
- [ ] Go/No-Go 决策

---

## 阻塞项 / 待确认问题

> ✅ **[已确认]** 部署方式：本地 Demo + Docker Compose（2026-02-21）
> 参见：[memory/2026-02-21.md](../memory/2026-02-21.md)

---

## 完成记录

| 时间 | 完成事项 | Memory 链接 |
|------|---------|------------|
| 2026-02-21 | Release 阶段框架搭建 | [memory/2026-02-21.md](../memory/2026-02-21.md) |
