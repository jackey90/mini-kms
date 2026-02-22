# IntelliKnow KMS — Data Model

## SQLite Schema

### Table: intent_spaces

Stores intent space definitions (HR, Legal, Finance + custom).

```sql
CREATE TABLE intent_spaces (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL UNIQUE,
    description TEXT    NOT NULL DEFAULT '',
    keywords    TEXT    NOT NULL DEFAULT '[]',  -- JSON array stored as text
    is_default  INTEGER NOT NULL DEFAULT 0,      -- 0=false, 1=true
    created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);

-- Seed default spaces
INSERT INTO intent_spaces (name, description, keywords, is_default) VALUES
('HR',      'Human resources policies, employee handbook, attendance, compensation, leave',
            '["HR","employee","leave","salary","policy","attendance","handbook"]', 1),
('Legal',   'Contract templates, legal terms, compliance policies, NDAs',
            '["contract","compliance","legal","NDA","policy","terms"]', 1),
('Finance', 'Expense reimbursement, budget policy, financial reports, procurement',
            '["budget","expense","reimbursement","finance","invoice","procurement"]', 1);
```

---

### Table: documents

Stores document metadata. File content is on disk; vectors are in FAISS.

```sql
CREATE TABLE documents (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    filename         TEXT    NOT NULL,
    format           TEXT    NOT NULL CHECK(format IN ('pdf', 'docx')),
    size_bytes       INTEGER NOT NULL,
    file_path        TEXT    NOT NULL,              -- relative: uploads/{id}_{filename}
    intent_space_id  INTEGER NOT NULL REFERENCES intent_spaces(id),
    status           TEXT    NOT NULL DEFAULT 'pending'
                             CHECK(status IN ('pending','processing','processed','error')),
    chunk_count      INTEGER DEFAULT 0,
    access_count     INTEGER NOT NULL DEFAULT 0,
    error_message    TEXT    DEFAULT NULL,
    uploaded_at      TEXT    NOT NULL DEFAULT (datetime('now')),
    processed_at     TEXT    DEFAULT NULL
);

CREATE INDEX idx_documents_intent_space ON documents(intent_space_id);
CREATE INDEX idx_documents_status ON documents(status);
```

---

### Table: query_logs

Stores every query submitted through any channel.

```sql
CREATE TABLE query_logs (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp         TEXT    NOT NULL DEFAULT (datetime('now')),
    user_query        TEXT    NOT NULL,
    detected_intent   TEXT    NOT NULL,          -- intent space name or "general"
    confidence_score  REAL    NOT NULL,
    source_documents  TEXT    NOT NULL DEFAULT '[]',  -- JSON array of filenames
    response_status   TEXT    NOT NULL CHECK(response_status IN ('success','fallback','error')),
    channel           TEXT    NOT NULL CHECK(channel IN ('telegram','teams','api')),
    user_id           TEXT    DEFAULT NULL,
    response_time_ms  INTEGER DEFAULT NULL
);

CREATE INDEX idx_query_logs_timestamp ON query_logs(timestamp);
CREATE INDEX idx_query_logs_intent ON query_logs(detected_intent);
CREATE INDEX idx_query_logs_channel ON query_logs(channel);
```

---

### Table: integrations

Stores bot integration credentials (tokens stored encrypted in env, only metadata here).

```sql
CREATE TABLE integrations (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    channel         TEXT    NOT NULL UNIQUE CHECK(channel IN ('telegram','teams')),
    name            TEXT    NOT NULL,
    token_last4     TEXT    DEFAULT NULL,   -- last 4 chars for display only
    status          TEXT    NOT NULL DEFAULT 'disconnected'
                            CHECK(status IN ('connected','disconnected','error')),
    last_active_at  TEXT    DEFAULT NULL,
    error_message   TEXT    DEFAULT NULL,
    updated_at      TEXT    NOT NULL DEFAULT (datetime('now'))
);

-- Seed integration rows (credentials come from env vars)
INSERT INTO integrations (channel, name) VALUES
('telegram', 'Telegram'),
('teams',    'Microsoft Teams');
```

---

## ER Diagram (text)

```
intent_spaces (1) ──< documents (N)
                        │
                        │  (access_count incremented by query_logs)
                        │
query_logs  (standalone — references intent space by name, not FK)

integrations  (standalone — no FK relationships)
```

---

## FAISS Index Files (not SQLite)

Stored at `data/faiss/` alongside the SQLite database:

```
data/
├── intelliknow.db                  ← SQLite database
├── faiss/
│   ├── intent_1.index              ← FAISS IndexFlatL2 for HR
│   ├── intent_1_meta.json          ← chunk→document mapping for HR
│   ├── intent_2.index              ← FAISS index for Legal
│   ├── intent_2_meta.json
│   ├── intent_3.index              ← FAISS index for Finance
│   └── intent_3_meta.json
└── uploads/
    ├── 1_hr-policy.pdf
    └── 2_employee-handbook.docx
```

### FAISS meta JSON format

```json
{
  "chunks": [
    {
      "faiss_id": 0,
      "document_id": 1,
      "filename": "hr-policy.pdf",
      "chunk_text": "Employees are entitled to 15 days of annual leave..."
    }
  ]
}
```

This meta file is the bridge between FAISS vector IDs and actual document/chunk content, enabling citations in responses.

---

## Notes

- SQLite WAL mode enabled for better concurrent read performance.
- `keywords` in `intent_spaces` is a JSON array serialized as TEXT (no need for a join table at MVP scale).
- `source_documents` in `query_logs` is a JSON array serialized as TEXT.
- FAISS indexes are rebuilt from scratch if the meta JSON goes out of sync (use `POST /documents/{id}/reparse`).
