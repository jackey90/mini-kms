import streamlit as st
import pandas as pd
from utils import api_client
from utils.helpers import format_datetime, format_size, status_badge

st.set_page_config(page_title="KB Management — IntelliKnow KMS", page_icon="📂", layout="wide")
st.title("📂 Knowledge Base Management")

# --- Upload section ---
st.subheader("Upload Document")

try:
    intents = api_client.get_intents()
except Exception as exc:
    st.error(f"Cannot load intent spaces: {exc}")
    st.stop()

intent_options = {s["name"]: s["id"] for s in intents}

with st.form("upload_form"):
    uploaded_file = st.file_uploader(
        "Choose a PDF or DOCX file (max 50MB)",
        type=["pdf", "docx"],
        label_visibility="visible",
    )
    selected_intent = st.selectbox("Intent Space", options=list(intent_options.keys()))
    submit = st.form_submit_button("Upload & Parse", type="primary")

if submit:
    if uploaded_file is None:
        st.warning("Please select a file before uploading.")
    else:
        with st.spinner(f"Uploading and parsing {uploaded_file.name}..."):
            try:
                result = api_client.upload_document(
                    file_bytes=uploaded_file.read(),
                    filename=uploaded_file.name,
                    intent_space_id=intent_options[selected_intent],
                )
                if result["status"] == "processed":
                    st.success(f"✅ '{uploaded_file.name}' parsed successfully ({result['chunk_count']} chunks)")
                elif result["status"] == "error":
                    st.error(f"❌ Parsing failed: {result.get('error_message', 'Unknown error')}")
                else:
                    st.info(f"Document uploaded with status: {result['status']}")
            except Exception as exc:
                st.error(f"Upload failed: {exc}")

st.divider()

# --- Document list ---
st.subheader("Documents")

col1, col2 = st.columns([3, 2])
with col1:
    search = st.text_input("Search by name", placeholder="e.g. hr-policy")
with col2:
    filter_intent = st.selectbox("Filter by Intent Space", ["All"] + list(intent_options.keys()))

try:
    intent_filter_id = intent_options.get(filter_intent) if filter_intent != "All" else None
    docs = api_client.get_documents(intent_space_id=intent_filter_id, search=search or None)
except Exception as exc:
    st.error(f"Failed to load documents: {exc}")
    docs = []

if not docs:
    st.info("No documents found. Upload a PDF or DOCX file above to get started.")
else:
    st.caption(f"{len(docs)} document(s)")

    for doc in docs:
        with st.container():
            c1, c2, c3, c4, c5, c6, c7 = st.columns([3, 2, 1, 1, 2, 1, 1])
            c1.write(f"📄 {doc['filename']}")
            c2.write(format_datetime(doc["uploaded_at"]))
            c3.write(doc["format"].upper())
            c4.write(format_size(doc["size_bytes"]))
            c5.write(status_badge(doc["status"]))
            if c6.button("🔄", key=f"reparse_{doc['id']}", help="Re-parse document"):
                with st.spinner("Re-parsing..."):
                    try:
                        result = api_client.reparse_document(doc["id"])
                        if result["status"] == "processed":
                            st.success(f"Re-parsed '{doc['filename']}' ({result['chunk_count']} chunks)")
                        else:
                            st.error(f"Re-parse failed: {result.get('error_message', 'Unknown')}")
                        st.rerun()
                    except Exception as exc:
                        st.error(f"Re-parse failed: {exc}")
            if c7.button("🗑️", key=f"del_{doc['id']}", help="Delete document"):
                if st.session_state.get(f"confirm_del_{doc['id']}"):
                    try:
                        api_client.delete_document(doc["id"])
                        st.success(f"Deleted '{doc['filename']}'")
                        st.rerun()
                    except Exception as exc:
                        st.error(f"Delete failed: {exc}")
                else:
                    st.session_state[f"confirm_del_{doc['id']}"] = True
                    st.warning(f"Click 🗑️ again to confirm deleting '{doc['filename']}'")
        st.divider()
