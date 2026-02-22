# IntelliKnow KMS — REST API Contract

Base URL: `http://localhost:8000/api`

All responses: `Content-Type: application/json`
Error format: `{ "detail": "error message" }`

---

## Health

### GET /health
Returns service status.

**Response 200**:
```json
{ "status": "ok", "version": "1.0.0" }
```

---

## Documents

### POST /documents
Upload and parse a document.

**Request**: `multipart/form-data`
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| file | file | ✅ | PDF or DOCX file, ≤ 50MB |
| intent_space_id | int | ✅ | ID of the intent space to associate |

**Response 201**:
```json
{
  "id": 1,
  "filename": "hr-policy.pdf",
  "format": "pdf",
  "size_bytes": 102400,
  "intent_space_id": 1,
  "intent_space_name": "HR",
  "status": "processing",
  "uploaded_at": "2026-02-21T10:00:00Z"
}
```

**Errors**:
- `400` — Unsupported file type or file too large
- `404` — intent_space_id not found

---

### GET /documents
List all documents with optional filters.

**Query Params**:
| Param | Type | Description |
|-------|------|-------------|
| intent_space_id | int | Filter by intent space |
| search | string | Search by filename |
| status | string | Filter by status (pending/processing/processed/error) |

**Response 200**:
```json
[
  {
    "id": 1,
    "filename": "hr-policy.pdf",
    "format": "pdf",
    "size_bytes": 102400,
    "intent_space_id": 1,
    "intent_space_name": "HR",
    "status": "processed",
    "chunk_count": 42,
    "access_count": 5,
    "uploaded_at": "2026-02-21T10:00:00Z"
  }
]
```

---

### GET /documents/{id}
Get single document details.

**Response 200**: Same as document object above.
**Errors**: `404` — Document not found

---

### DELETE /documents/{id}
Delete a document and remove its vectors from FAISS.

**Response 200**:
```json
{ "message": "Document deleted successfully" }
```

**Errors**: `404` — Document not found

---

### POST /documents/{id}/reparse
Re-parse and re-vectorize an existing document (P2).

**Response 202**:
```json
{ "message": "Re-parsing started", "document_id": 1 }
```

---

## Intent Spaces

### POST /intents
Create a new intent space.

**Request Body**:
```json
{
  "name": "Operations",
  "description": "Operational procedures and guidelines",
  "keywords": ["SOP", "workflow", "operations", "process"]
}
```

**Response 201**:
```json
{
  "id": 4,
  "name": "Operations",
  "description": "Operational procedures and guidelines",
  "keywords": ["SOP", "workflow", "operations", "process"],
  "document_count": 0,
  "is_default": false,
  "created_at": "2026-02-21T10:00:00Z"
}
```

**Errors**: `400` — Name already exists

---

### GET /intents
List all intent spaces.

**Response 200**:
```json
[
  {
    "id": 1,
    "name": "HR",
    "description": "Human resources policies and procedures",
    "keywords": ["HR", "employee", "leave", "salary", "policy"],
    "document_count": 3,
    "is_default": true,
    "created_at": "2026-02-21T10:00:00Z"
  },
  {
    "id": 2,
    "name": "Legal",
    "description": "Legal terms, contracts, and compliance",
    "keywords": ["contract", "compliance", "legal", "NDA"],
    "document_count": 2,
    "is_default": true,
    "created_at": "2026-02-21T10:00:00Z"
  },
  {
    "id": 3,
    "name": "Finance",
    "description": "Finance, budgeting, and expense policies",
    "keywords": ["budget", "expense", "reimbursement", "finance"],
    "document_count": 1,
    "is_default": true,
    "created_at": "2026-02-21T10:00:00Z"
  }
]
```

---

### PUT /intents/{id}
Update an intent space.

**Request Body** (all fields optional):
```json
{
  "name": "HR",
  "description": "Updated description",
  "keywords": ["HR", "employee", "attendance"]
}
```

**Response 200**: Updated intent space object.
**Errors**: `404` — Not found | `400` — Name conflict

---

### DELETE /intents/{id}
Delete an intent space. Fails if documents are associated.

**Response 200**:
```json
{ "message": "Intent space deleted successfully" }
```

**Errors**:
- `404` — Not found
- `400` — Cannot delete: documents are associated
- `400` — Cannot delete default intent spaces

---

## Query

### POST /query
Submit a query for intent classification and RAG retrieval.

**Request Body**:
```json
{
  "query": "What is the annual leave policy?",
  "channel": "telegram",
  "user_id": "telegram_user_123"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| query | string | ✅ | User's question |
| channel | string | ✅ | `telegram` or `teams` |
| user_id | string | ❌ | Platform user identifier |

**Response 200**:
```json
{
  "query_id": 42,
  "answer": "Employees are entitled to 15 days of annual leave per year...",
  "detected_intent": "HR",
  "confidence": 0.92,
  "source_documents": ["hr-policy.pdf"],
  "channel_formatted": "Employees are entitled to 15 days of annual leave per year...\n\n📄 Source: hr-policy.pdf",
  "fallback": false
}
```

**Fallback response** (confidence < 0.7 or no relevant content):
```json
{
  "query_id": 43,
  "answer": "I couldn't find relevant information in the knowledge base.",
  "detected_intent": "general",
  "confidence": 0.45,
  "source_documents": [],
  "channel_formatted": "I couldn't find relevant information in the knowledge base.",
  "fallback": true
}
```

**Errors**: `422` — Empty query

---

## Integrations

### GET /integrations
Get status of all configured integrations.

**Response 200**:
```json
[
  {
    "id": 1,
    "name": "Telegram",
    "channel": "telegram",
    "status": "connected",
    "token_last4": "a8f2",
    "last_active_at": "2026-02-21T09:55:00Z",
    "error_message": null
  },
  {
    "id": 2,
    "name": "Microsoft Teams",
    "channel": "teams",
    "status": "disconnected",
    "token_last4": null,
    "last_active_at": null,
    "error_message": null
  }
]
```

---

### PUT /integrations/{channel}
Configure an integration (channel = `telegram` or `teams`).

**Request Body** for Telegram:
```json
{ "bot_token": "1234567890:ABCdef..." }
```

**Request Body** for Teams:
```json
{
  "app_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "app_password": "your-app-password"
}
```

**Response 200**:
```json
{ "message": "Integration configured successfully", "status": "connected" }
```

**Errors**: `400` — Invalid credentials

---

### POST /integrations/{channel}/test
Send a test message to verify the integration.

**Response 200**:
```json
{
  "success": true,
  "response_time_ms": 245,
  "message": "Test message sent and acknowledged successfully"
}
```

**Response 200** (failure):
```json
{
  "success": false,
  "response_time_ms": null,
  "message": "Failed to connect: Invalid bot token"
}
```

---

## Analytics

### GET /analytics/queries
Get query history log.

**Query Params**:
| Param | Type | Description |
|-------|------|-------------|
| limit | int | Records per page (default: 50, max: 200) |
| offset | int | Pagination offset (default: 0) |
| intent | string | Filter by detected intent |
| channel | string | Filter by channel (telegram/teams) |
| date_from | string | ISO date string (e.g. 2026-02-01) |
| date_to | string | ISO date string |

**Response 200**:
```json
{
  "total": 124,
  "items": [
    {
      "id": 42,
      "timestamp": "2026-02-21T09:55:00Z",
      "user_query": "What is the annual leave policy?",
      "detected_intent": "HR",
      "confidence_score": 0.92,
      "source_documents": ["hr-policy.pdf"],
      "response_status": "success",
      "channel": "telegram",
      "response_time_ms": 1850
    }
  ]
}
```

---

### GET /analytics/kb-usage
Get knowledge base usage statistics.

**Response 200**:
```json
{
  "total_documents": 6,
  "total_queries": 124,
  "intent_distribution": [
    { "intent": "HR", "count": 68 },
    { "intent": "Legal", "count": 31 },
    { "intent": "Finance", "count": 18 },
    { "intent": "general", "count": 7 }
  ],
  "top_documents": [
    { "filename": "hr-policy.pdf", "access_count": 45 },
    { "filename": "employee-handbook.pdf", "access_count": 23 }
  ]
}
```

---

### GET /analytics/export
Export query logs as CSV.

**Response 200**: `Content-Type: text/csv`

CSV columns: `id,timestamp,user_query,detected_intent,confidence_score,source_documents,response_status,channel,response_time_ms`

---

## Error Codes Reference

| HTTP Status | Meaning |
|-------------|---------|
| 200 | OK |
| 201 | Created |
| 202 | Accepted (async operation started) |
| 400 | Bad Request (validation error) |
| 404 | Not Found |
| 422 | Unprocessable Entity (Pydantic validation) |
| 500 | Internal Server Error |
