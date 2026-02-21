# Frontend 阶段状态

> 对应开发流程：Phase 5.1 前端研发（Frontend）

**阶段目标**：实现 IntelliKnow KMS Admin Dashboard（5个核心页面），对接后端 REST API。

**前置条件**：`architecture/STATUS.md` 中 API Contract 和 UI 线框图已完成。

---

## 5.1 项目初始化

- [ ] 技术栈确认（Next.js / Streamlit — 依赖 architecture 阶段决策）
- [ ] 项目脚手架搭建
- [ ] 路由结构设计
- [ ] 通用组件库 / UI 框架选择（Tailwind CSS、shadcn/ui 等）
- [ ] API 客户端封装（统一请求层）

## 5.2 Admin Dashboard 页面

### Dashboard 主页
- [ ] 4个功能模块卡片（Frontend Integration / KB Management / Intent Config / Analytics）
- [ ] 状态概览（已连接集成数、文档总数、今日查询数）
- [ ] 导航栏（顶部或侧边）

### KB Management 页面
- [ ] 文档列表（名称 / 上传时间 / 格式 / 大小 / 状态 / 操作）
- [ ] 拖拽上传区（支持 PDF/DOCX，带进度指示器）
- [ ] 搜索栏（按名称/关键词）
- [ ] 格式/日期/意图空间筛选器
- [ ] 文档删除 / 重新解析操作

### Intent Configuration 页面
- [ ] 意图空间卡片列表（名称 / 描述 / 关联文档数 / 分类准确率）
- [ ] 查询分类日志表格（查询内容 / 意图 / 置信度 / 响应状态）
- [ ] 意图空间创建/编辑表单

### Frontend Integration 页面
- [ ] 集成状态卡片（每个工具：Connected/Disconnected 状态指示）
- [ ] 配置详情（API Key 末4位、Webhook URL 等）
- [ ] 测试按钮（发送示例查询验证集成）
- [ ] 配置编辑表单

### Analytics 页面
- [ ] 查询历史表格（时间戳 / 意图 / 置信度 / 响应状态）
- [ ] KB 使用统计（最常访问文档、各意图空间查询量）
- [ ] 数据导出按钮

## 5.3 状态管理

- [ ] 全局状态管理（React Context 或 Zustand）
- [ ] API 数据缓存策略
- [ ] 加载/错误状态处理

## 5.4 测试

- [ ] 组件单元测试（关键组件）
- [ ] 页面集成测试

## 5.5 性能与兼容性

- [ ] 响应式设计（桌面优先，可选移动端）
- [ ] 加载性能优化

---

## 阻塞项 / 待确认问题

> ❗ **[阻塞]** 等待 architecture 阶段确认前端框架选型（Next.js vs Streamlit）
> ❗ **[阻塞]** 等待 architecture 阶段完成 API Contract

---

## 完成记录

| 时间 | 完成事项 | Memory 链接 |
|------|---------|------------|
| 2026-02-21 | 前端阶段框架搭建 | [memory/2026-02-21.md](../memory/2026-02-21.md) |
