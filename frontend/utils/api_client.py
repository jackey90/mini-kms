import os
import requests

BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000/api")


def _get(path: str, params: dict | None = None) -> dict | list:
    resp = requests.get(f"{BASE_URL}{path}", params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def _post(path: str, json: dict | None = None) -> dict:
    resp = requests.post(f"{BASE_URL}{path}", json=json, timeout=30)
    resp.raise_for_status()
    return resp.json()


def _put(path: str, json: dict) -> dict:
    resp = requests.put(f"{BASE_URL}{path}", json=json, timeout=30)
    resp.raise_for_status()
    return resp.json()


def _delete(path: str) -> dict:
    resp = requests.delete(f"{BASE_URL}{path}", timeout=30)
    resp.raise_for_status()
    return resp.json()


# --- Documents ---

def get_documents(intent_space_id: int | None = None, search: str | None = None) -> list:
    params = {}
    if intent_space_id:
        params["intent_space_id"] = intent_space_id
    if search:
        params["search"] = search
    return _get("/documents", params=params)


def upload_document(file_bytes: bytes, filename: str, intent_space_id: int) -> dict:
    resp = requests.post(
        f"{BASE_URL}/documents",
        files={"file": (filename, file_bytes)},
        data={"intent_space_id": str(intent_space_id)},
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()


def reparse_document(doc_id: int) -> dict:
    return _post(f"/documents/{doc_id}/reparse")


def delete_document(doc_id: int) -> dict:
    return _delete(f"/documents/{doc_id}")


# --- Intent Spaces ---

def get_intents() -> list:
    return _get("/intents")


def create_intent(name: str, description: str, keywords: list[str]) -> dict:
    return _post("/intents", {"name": name, "description": description, "keywords": keywords})


def update_intent(space_id: int, name: str, description: str, keywords: list[str]) -> dict:
    return _put(f"/intents/{space_id}", {"name": name, "description": description, "keywords": keywords})


def delete_intent(space_id: int) -> dict:
    return _delete(f"/intents/{space_id}")


# --- Query ---

def submit_query(query: str, channel: str = "api") -> dict:
    return _post("/query", {"query": query, "channel": channel})


# --- Integrations ---

def get_integrations() -> list:
    return _get("/integrations")


def configure_telegram(bot_token: str) -> dict:
    return _put("/integrations/telegram", {"bot_token": bot_token})


def configure_teams(app_id: str, app_password: str) -> dict:
    return _put("/integrations/teams", {"app_id": app_id, "app_password": app_password})


def test_integration(channel: str) -> dict:
    return _post(f"/integrations/{channel}/test")


# --- Analytics ---

def get_query_logs(limit: int = 50, offset: int = 0, intent: str | None = None,
                   channel: str | None = None) -> dict:
    params: dict = {"limit": limit, "offset": offset}
    if intent:
        params["intent"] = intent
    if channel:
        params["channel"] = channel
    return _get("/analytics/queries", params=params)


def get_kb_stats() -> dict:
    return _get("/analytics/kb-usage")


def get_export_url() -> str:
    return f"{BASE_URL}/analytics/export"


def reclassify_query(query_id: int, correct_intent: str) -> dict:
    return _put(f"/analytics/queries/{query_id}/reclassify", {"correct_intent": correct_intent})


def export_csv() -> bytes:
    resp = requests.get(f"{BASE_URL}/analytics/export", timeout=30)
    resp.raise_for_status()
    return resp.content


# --- Health ---

def health_check() -> bool:
    try:
        r = requests.get(f"{BASE_URL}/health", timeout=3)
        return r.status_code == 200
    except Exception:
        return False
