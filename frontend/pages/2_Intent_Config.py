import streamlit as st
import pandas as pd
from utils import api_client
from utils.helpers import format_datetime, truncate

st.set_page_config(page_title="Intent Configuration — IntelliKnow KMS", page_icon="🎯", layout="wide")
st.title("🎯 Intent Space Configuration")

# --- Load intent spaces ---
try:
    intents = api_client.get_intents()
except Exception as exc:
    st.error(f"Cannot load intent spaces: {exc}")
    st.stop()

# --- Add new intent space ---
with st.expander("➕ Add New Intent Space"):
    with st.form("create_intent_form"):
        new_name = st.text_input("Name *", placeholder="e.g. Operations")
        new_desc = st.text_area("Description", placeholder="What topics does this space cover?")
        new_kw = st.text_input("Keywords (comma-separated)", placeholder="SOP, workflow, operations")
        created = st.form_submit_button("Create Intent Space", type="primary")

    if created:
        if not new_name.strip():
            st.warning("Name is required.")
        else:
            keywords = [k.strip() for k in new_kw.split(",") if k.strip()]
            try:
                api_client.create_intent(new_name.strip(), new_desc, keywords)
                st.success(f"✅ Intent space '{new_name}' created!")
                st.rerun()
            except Exception as exc:
                st.error(f"Failed: {exc}")

st.divider()

# --- Intent Space Cards ---
st.subheader("Intent Spaces")
cols = st.columns(min(len(intents), 3))
for i, space in enumerate(intents):
    with cols[i % 3]:
        badge = "🔒" if space["is_default"] else "✏️"
        st.markdown(f"**{badge} {space['name']}**")
        st.caption(space["description"] or "No description")
        st.write(f"📄 {space['document_count']} document(s)")
        kw_str = ", ".join(space["keywords"][:5])
        if kw_str:
            st.caption(f"Keywords: {kw_str}")

        with st.expander("Edit"):
            with st.form(f"edit_{space['id']}"):
                e_name = st.text_input("Name", value=space["name"])
                e_desc = st.text_area("Description", value=space["description"])
                e_kw = st.text_input("Keywords", value=", ".join(space["keywords"]))
                saved = st.form_submit_button("Save")
            if saved:
                kw_list = [k.strip() for k in e_kw.split(",") if k.strip()]
                try:
                    api_client.update_intent(space["id"], e_name, e_desc, kw_list)
                    st.success("Saved!")
                    st.rerun()
                except Exception as exc:
                    st.error(str(exc))

        if not space["is_default"]:
            if st.button(f"🗑️ Delete", key=f"del_space_{space['id']}"):
                try:
                    api_client.delete_intent(space["id"])
                    st.success(f"Deleted '{space['name']}'")
                    st.rerun()
                except Exception as exc:
                    st.error(str(exc))

st.divider()

# --- Query Classification Log ---
st.subheader("Recent Query Classification Log")
try:
    logs_page = api_client.get_query_logs(limit=20)
    items = logs_page.get("items", [])
except Exception as exc:
    st.error(f"Failed to load logs: {exc}")
    items = []

if items:
    rows = [
        {
            "Time": format_datetime(item["timestamp"]),
            "Query": truncate(item["user_query"], 55),
            "Intent": item["detected_intent"],
            "Confidence": f"{item['confidence_score']:.0%}",
            "Status": item["response_status"],
            "Channel": item["channel"],
        }
        for item in items
    ]
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
else:
    st.info("No queries yet.")
