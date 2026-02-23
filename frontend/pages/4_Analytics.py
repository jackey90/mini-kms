import streamlit as st
import pandas as pd
from utils import api_client
from utils.helpers import format_datetime, truncate

st.set_page_config(page_title="Analytics — IntelliKnow KMS", page_icon="📈", layout="wide")
st.title("📈 Analytics & Query History")

# --- Filters ---
st.subheader("Filters")
col1, col2, col3 = st.columns(3)
with col1:
    intent_filter = st.selectbox("Intent", ["All", "HR", "Legal", "Finance", "general"])
with col2:
    channel_filter = st.selectbox("Channel", ["All", "telegram", "teams", "api"])
with col3:
    limit = st.selectbox("Show", [20, 50, 100, 200], index=1)

intent_param = None if intent_filter == "All" else intent_filter
channel_param = None if channel_filter == "All" else channel_filter

# --- KB Stats ---
try:
    stats = api_client.get_kb_stats()
except Exception as exc:
    st.error(f"Failed to load stats: {exc}")
    stats = {}

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Documents", stats.get("total_documents", 0))
col2.metric("Total Queries", stats.get("total_queries", 0))
col3.metric("Avg Latency", f"{stats.get('avg_latency_ms', 0)} ms")
col4.metric("Intent Spaces Active", len(stats.get("intent_distribution", [])))

st.divider()

# --- Intent Distribution ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Intent Distribution")
    dist = stats.get("intent_distribution", [])
    if dist:
        df_dist = pd.DataFrame(dist).rename(columns={"intent": "Intent", "count": "Queries"})
        st.bar_chart(df_dist.set_index("Intent"))
    else:
        st.info("No query data yet.")

with col_right:
    st.subheader("Top Accessed Documents")
    top_docs = stats.get("top_documents", [])
    if top_docs:
        df_docs = pd.DataFrame(top_docs).rename(
            columns={"filename": "Document", "access_count": "Accesses"}
        )
        st.dataframe(df_docs, use_container_width=True, hide_index=True)
    else:
        st.info("No document access data yet.")

st.divider()

# --- CSV Export ---
st.subheader("Export")
try:
    csv_data = api_client.export_csv()
    st.download_button(
        label="⬇️ Export Query Logs (CSV)",
        data=csv_data,
        file_name="intelliknow_query_logs.csv",
        mime="text/csv",
    )
except Exception as exc:
    st.error(f"Export failed: {exc}")

st.divider()

# --- Query History Table ---
st.subheader("Query History")
try:
    logs_page = api_client.get_query_logs(limit=limit, intent=intent_param, channel=channel_param)
    items = logs_page.get("items", [])
    total = logs_page.get("total", 0)
except Exception as exc:
    st.error(f"Failed to load query logs: {exc}")
    items = []
    total = 0

st.caption(f"Showing {len(items)} of {total} queries")

if items:
    rows = [
        {
            "Time": format_datetime(item["timestamp"]),
            "Query": truncate(item["user_query"], 60),
            "Intent": item["detected_intent"],
            "Confidence": f"{item['confidence_score']:.0%}",
            "Sources": ", ".join(item["source_documents"]) if item["source_documents"] else "—",
            "Channel": item["channel"],
            "Status": item["response_status"],
            "Time (ms)": item["response_time_ms"],
        }
        for item in items
    ]
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
else:
    st.info("No queries match the selected filters.")
