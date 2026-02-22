import streamlit as st
import pandas as pd
from utils import api_client
from utils.helpers import format_datetime, truncate, status_badge

st.set_page_config(
    page_title="IntelliKnow KMS",
    page_icon="🧠",
    layout="wide",
)

# Sidebar backend health indicator
with st.sidebar:
    st.title("🧠 IntelliKnow KMS")
    st.divider()
    alive = api_client.health_check()
    st.caption(f"Backend: {'🟢 Connected' if alive else '🔴 Offline'}")

st.title("📊 Dashboard")
st.caption("Overview of your Knowledge Management System")

if not alive:
    st.error("⚠️ Cannot connect to backend (http://localhost:8000). Make sure the backend is running.")
    st.stop()

# Fetch summary data
try:
    docs = api_client.get_documents()
    intents = api_client.get_intents()
    integrations = api_client.get_integrations()
    stats = api_client.get_kb_stats()
    logs_page = api_client.get_query_logs(limit=5)
except Exception as exc:
    st.error(f"Failed to load data: {exc}")
    st.stop()

# --- Top metrics ---
col1, col2, col3, col4 = st.columns(4)

connected = sum(1 for i in integrations if i["status"] == "connected")
col1.metric("Integrations", f"{connected}/{len(integrations)}", "Connected")

processed = sum(1 for d in docs if d["status"] == "processed")
col2.metric("Documents", processed, "Processed")

col3.metric("Intent Spaces", len(intents))

col4.metric("Total Queries", stats.get("total_queries", 0))

st.divider()

# --- Recent queries ---
st.subheader("Recent Queries")
items = logs_page.get("items", [])
if items:
    rows = []
    for item in items:
        rows.append({
            "Time": format_datetime(item["timestamp"]),
            "Query": truncate(item["user_query"], 60),
            "Intent": item["detected_intent"],
            "Confidence": f"{item['confidence_score']:.0%}",
            "Channel": item["channel"],
            "Status": status_badge(item["response_status"]),
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
else:
    st.info("No queries yet. Send a message via Telegram or Teams to see activity here.")
