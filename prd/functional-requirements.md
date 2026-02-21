# IntelliKnow KMS — 功能需求（Functional Requirements）

> 格式：用户故事 + 功能点 + 备注
> 优先级：P0（必须）/ P1（应该）/ P2（可选）

---

## FR-01 多前端集成（Multi-Frontend Integration）

**目标用户**：Admin（配置）、End User（使用）

### FR-01-1: Telegram Bot 集成（P0）

**用户故事**：
> 作为员工，我希望在 Telegram 中直接向 Bot 发送问题，并在 3 秒内收到来自企业知识库的回答，这样我不需要打开任何额外的网页。

**功能点**：
- Admin 在 Frontend Integration 页面配置 Telegram Bot Token
- Bot 使用 Polling 模式监听消息（本地 Demo，无需 Webhook）
- 接收用户消息后，调用查询 API（FR-03 + FR-04）获取回答
- 将回答格式化后回复给用户（纯文本 + 来源引用）
- 支持 `/start` 命令返回使用说明

**Telegram 响应格式**：
```
[回答内容]

📄 Source: [文档名称]
```

---

### FR-01-2: Microsoft Teams Bot 集成（P1）

**用户故事**：
> 作为企业员工，我希望在 Microsoft Teams 中向 Bot 提问，获得与 Telegram 相同质量的知识库回答。

**功能点**：
- Admin 在 Frontend Integration 页面配置 Teams App ID + App Password
- 使用 Bot Framework SDK（`botbuilder-python`）处理消息
- 本地 Demo 使用 Bot Framework Emulator 或 ngrok 测试
- 消息路由到同一查询 API
- 响应格式适配 Teams（支持 Adaptive Card 或纯文本）

**Teams 响应格式**：
```
[回答内容]

Source: [文档名称]
```

---

### FR-01-3: 连接状态监控（P1）

**用户故事**：
> 作为 Admin，我希望在 Frontend Integration 页面看到每个集成的连接状态，以便快速发现配置问题。

**功能点**：
- 每个集成显示状态：`Connected` / `Disconnected` / `Error`
- 显示最后一次成功消息的时间戳
- 配置详情显示（API Key 末4位，不显示完整密钥）

---

### FR-01-4: 集成测试功能（P1）

**用户故事**：
> 作为 Admin，我希望点击"Test"按钮向指定集成发送一条测试消息，验证连接是否正常。

**功能点**：
- Test 按钮触发发送预设测试消息（"Hello, this is a test message from IntelliKnow KMS"）
- 显示测试结果（成功/失败 + 响应时间）

---

## FR-02 文档驱动知识库（Document-Driven Knowledge Base）

**目标用户**：Admin

### FR-02-1: PDF 文档上传与解析（P0）

**用户故事**：
> 作为 Admin，我希望上传一份 PDF 文件后，系统自动解析其内容并加入知识库，这样员工的查询就能基于这份文档回答。

**功能点**：
- 支持拖拽上传或文件选择器
- 文件大小限制：≤ 50MB
- 使用 LangChain `PyPDFLoader` 解析文本内容（包括带表格的页面）
- 文本分块：`RecursiveCharacterTextSplitter`（chunk_size=500, chunk_overlap=50）
- 向量化：OpenAI `text-embedding-3-small`，存入 FAISS 索引
- 元数据存入 SQLite（文件名、上传时间、状态、意图空间 ID、chunk 数量）
- 处理状态：`Pending` → `Processing` → `Processed` / `Error`
- 前端显示处理进度指示器

---

### FR-02-2: DOCX 文档上传与解析（P0）

**用户故事**：
> 作为 Admin，我希望上传 Word 文档（.docx），系统能正确提取文本内容并加入知识库。

**功能点**：
- 同 FR-02-1，使用 LangChain `Docx2txtLoader` 解析
- 支持包含表格的 DOCX（提取为纯文本）

---

### FR-02-3: 意图空间关联（P0）

**用户故事**：
> 作为 Admin，我希望在上传文档时指定它属于哪个意图空间（如 HR），这样 HR 相关查询只会在 HR 文档中检索。

**功能点**：
- 上传表单包含意图空间选择下拉框
- 一个文档只属于一个意图空间（MVP 限制）
- FAISS 索引按意图空间分区（每个意图空间独立索引）
- 已上传文档可重新分配意图空间（触发重新索引）

---

### FR-02-4: 文档删除（P1）

**功能点**：
- 文档列表支持单个删除
- 删除时同步从 FAISS 索引中移除对应向量
- 确认对话框防止误删

---

### FR-02-5: 文档重新解析（P2）

**功能点**：
- 文档列表支持"Reparse"操作
- 重新上传同名文件覆盖已有文档，触发重新解析

---

### FR-02-6: 基础错误处理（P0）

**功能点**：
- 上传不支持的格式：返回明确错误提示（"Only PDF and DOCX are supported"）
- 解析失败（如加密 PDF）：文档状态变为 `Error`，显示错误原因
- 文件过大：上传前校验，超过限制立即提示

---

### FR-02-7: 文档搜索与过滤（P1）

**功能点**：
- 按文档名搜索
- 按意图空间过滤
- 按上传时间排序

---

## FR-03 意图空间编排器（Orchestrator）

**目标用户**：Admin（配置）、系统（自动分类）

### FR-03-1: 默认意图空间（P0）

**功能点**：
- 系统初始化时创建3个默认意图空间：
  - **HR**：人力资源政策、员工手册、考勤、薪酬、年假
  - **Legal**：合同模板、法律条款、合规政策、保密协议
  - **Finance**：报销流程、预算政策、财务报表、采购审批
- 每个意图空间有：名称、描述、关键词列表（辅助分类）

---

### FR-03-2: 自定义意图空间 CRUD（P1）

**用户故事**：
> 作为 Admin，我希望创建自定义意图空间（如"Operations"），以支持更多知识域。

**功能点**：
- 创建：名称（必填）+ 描述（可选）+ 关键词（可选，逗号分隔）
- 编辑：修改名称/描述/关键词
- 删除：仅允许删除没有关联文档的意图空间

---

### FR-03-3: AI 意图分类（P0）

**功能点**：
- 用户查询到达时，使用 `gpt-3.5-turbo` 进行 zero-shot 分类
- Prompt 包含所有意图空间的名称 + 描述 + 关键词
- 返回：`{ "intent": "HR", "confidence": 0.85 }`
- 置信度阈值：≥ 0.7（默认值）
- 分类结果写入查询日志（FR-06-1）

---

### FR-03-4: 兜底路由（P0）

**功能点**：
- 置信度 < 0.7：路由到 `General` 空间（检索所有文档）
- `General` 是系统保留空间，不可删除
- Bot 响应中标明"未找到精确匹配的知识域，以下来自综合知识库"

---

### FR-03-5: 意图路由后 RAG 检索（P0）

**功能点**：
- 确定意图空间后，在该空间的 FAISS 索引中执行语义检索
- 检索 Top-5 相关 chunk
- 将 chunk 组装为上下文，传入 LLM 生成响应

---

## FR-04 知识检索与响应（Knowledge Retrieval & Response）

### FR-04-1: 带引用的 RAG 响应（P0）

**用户故事**：
> 作为员工，我希望 Bot 的回答中包含来源文档名称，这样我可以验证信息的准确性。

**功能点**：
- 响应格式：简洁回答（≤200字）+ 来源文档名称
- LLM Prompt 要求：回答必须基于提供的上下文，不可凭空生成
- 如果上下文不包含相关信息，明确说明"未在知识库中找到相关信息"

---

### FR-04-2: 多前端响应格式适配（P1）

**功能点**：
- Telegram：纯文本 + emoji 标注来源（`📄 Source:`）
- Teams：Adaptive Card（标题 + 内容 + 来源链接）或纯文本

---

### FR-04-3: 无匹配时的兜底响应（P0）

**功能点**：
- 知识库为空：返回"Knowledge base is empty. Please ask admin to upload documents."
- 检索结果相关性过低（similarity score < 0.5）：返回"I couldn't find relevant information in the knowledge base."
- Bot 保持友好语气，不返回裸错误信息

---

## FR-05 Admin UI

### FR-05-1: Dashboard 主页（P1）

**功能点**：
- 4个模块状态卡片（Frontend Integration / KB Management / Intent Config / Analytics）
- 每个卡片显示关键统计（连接数 / 文档数 / 意图空间数 / 今日查询数）
- 点击卡片跳转到对应页面
- 顶部/侧边导航栏

---

### FR-05-2: Frontend Integration 页面（P1）

**功能点**：
- 每个集成一张状态卡片（Telegram / Teams）
- 状态指示器：Connected（绿）/ Disconnected（灰）/ Error（红）
- 配置按钮：弹出配置表单（输入 Token/API Key）
- Test 按钮：发送测试消息
- 详情显示：Token 末4位、最后活跃时间

---

### FR-05-3: KB Management 页面（P0）

**功能点**：

文档列表（表格视图）：
- 列：文档名 / 上传时间 / 格式 / 大小 / 意图空间 / 状态 / 操作
- 状态标签颜色：Processed（绿）/ Processing（黄）/ Error（红）/ Pending（灰）
- 操作：删除

上传区：
- 拖拽上传 + 文件选择按钮
- 支持格式说明（PDF, DOCX）
- 上传时选择意图空间
- 上传进度条

搜索 + 过滤：
- 搜索框（按文档名）
- 意图空间下拉过滤器

---

### FR-05-4: Intent Configuration 页面（P0）

**功能点**：

意图空间列表（卡片视图）：
- 每个卡片：名称 / 描述 / 关联文档数 / 分类准确率（近7日）
- 操作：编辑 / 删除（有文档时禁用删除）
- "Add Intent Space" 按钮

查询分类日志（表格）：
- 列：时间 / 查询内容（截断50字）/ 识别意图 / 置信度 / 响应状态
- 分页（每页20条）

意图编辑表单（抽屉/弹窗）：
- 名称（必填）/ 描述 / 关键词（逗号分隔）
- 保存 / 取消

---

### FR-05-5: Analytics 页面（P1）

**功能点**：
- 查询历史完整列表（时间 / 意图 / 置信度 / 响应状态 / 来源文档）
- KB 使用统计：最常访问文档 Top 10
- 各意图空间查询量分布
- 日期范围过滤器
- 导出 CSV 按钮

---

## FR-06 分析与历史（Analytics & History）

### FR-06-1: 查询日志自动记录（P0）

**功能点**：
- 每次查询自动写入 SQLite `query_logs` 表
- 记录字段：id / timestamp / user_query / detected_intent / confidence_score / source_documents / response_status / channel（telegram/teams）

---

### FR-06-2: KB 使用情况追踪（P1）

**功能点**：
- 每次文档被检索命中，更新该文档的 `access_count` 计数器
- Analytics 页面展示文档访问热度排行

---

### FR-06-3: 数据导出（P2）

**功能点**：
- `GET /api/analytics/export` 返回 CSV 格式的查询日志
- 前端提供"Export CSV"按钮，触发下载
