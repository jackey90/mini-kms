import streamlit as st
from utils import api_client

st.set_page_config(page_title="Chat — IntelliKnow KMS", page_icon="💬", layout="wide")

# --- Session state init ---
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "chat_user_id" not in st.session_state:
    st.session_state.chat_user_id = "demo"

# --- Sidebar: user identity ---
with st.sidebar:
    st.header("👤 User Identity")
    st.session_state.chat_user_id = st.text_input(
        "User ID",
        value=st.session_state.chat_user_id,
        placeholder="e.g. alice, demo, user@company.com",
        help="Queries are logged under this ID. Change it to simulate a different user.",
    )
    st.caption("Queries are scoped to this user ID in the analytics log.")

    st.divider()
    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.chat_messages = []
        st.rerun()

    st.divider()
    st.caption("**Sample questions to try:**")
    samples = [
        "What is the annual leave policy?",
        "How does the company handle personal data?",
        "What was the revenue growth in Q4 2025?",
        "What are the reimbursement rules?",
    ]
    for sample in samples:
        if st.button(sample, use_container_width=True, key=f"sample_{sample[:20]}"):
            st.session_state["_prefill"] = sample
            st.rerun()

# --- Page header ---
st.title("💬 Chat with IntelliKnow KMS")
uid = st.session_state.chat_user_id or "anonymous"
st.caption(f"Querying as **{uid}** · Answers are retrieved from your uploaded knowledge base")

if not st.session_state.chat_user_id.strip():
    st.warning("Set a User ID in the sidebar before sending a message.")

st.divider()

# --- Render chat history ---
for msg in st.session_state.chat_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and "meta" in msg:
            meta = msg["meta"]
            confidence_pct = f"{meta['confidence']:.0%}"
            badge = "🟢" if meta["confidence"] >= 0.7 else "🟡"
            sources = ", ".join(meta["source_documents"]) if meta["source_documents"] else "—"
            fallback_note = " · ⚠️ Fallback (low confidence)" if meta.get("fallback") else ""
            with st.expander(
                f"{badge} Intent: **{meta['detected_intent']}** · Confidence: {confidence_pct} · {meta['response_time_ms']}ms{fallback_note}",
                expanded=False,
            ):
                st.markdown(f"**Sources:** {sources}")
                st.markdown(f"**Query ID:** {meta['query_id']}")
                st.markdown(f"**Channel:** {meta['channel_formatted']}")

# --- Chat input ---
prefill = st.session_state.pop("_prefill", None)
user_input = st.chat_input("Ask anything from the knowledge base…", key="chat_input")

query_text = prefill or user_input

if query_text:
    user_id = st.session_state.chat_user_id.strip() or None

    # Show user message
    st.session_state.chat_messages.append({"role": "user", "content": query_text})
    with st.chat_message("user"):
        st.markdown(query_text)

    # Call API and stream response
    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            try:
                result = api_client.submit_query(query_text, channel="web", user_id=user_id)
                answer = result["answer"]
                st.markdown(answer)

                meta = {
                    "query_id": result["query_id"],
                    "detected_intent": result["detected_intent"],
                    "confidence": result["confidence"],
                    "source_documents": result["source_documents"],
                    "fallback": result["fallback"],
                    "response_time_ms": result["response_time_ms"],
                    "channel_formatted": result["channel_formatted"],
                }

                confidence_pct = f"{meta['confidence']:.0%}"
                badge = "🟢" if meta["confidence"] >= 0.7 else "🟡"
                sources = ", ".join(meta["source_documents"]) if meta["source_documents"] else "—"
                fallback_note = " · ⚠️ Fallback (low confidence)" if meta["fallback"] else ""
                with st.expander(
                    f"{badge} Intent: **{meta['detected_intent']}** · Confidence: {confidence_pct} · {meta['response_time_ms']}ms{fallback_note}",
                    expanded=False,
                ):
                    st.markdown(f"**Sources:** {sources}")
                    st.markdown(f"**Query ID:** {meta['query_id']}")
                    st.markdown(f"**Channel:** {meta['channel_formatted']}")

                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": answer,
                    "meta": meta,
                })

            except Exception as exc:
                error_msg = f"⚠️ Error: {exc}"
                st.error(error_msg)
                st.session_state.chat_messages.append({"role": "assistant", "content": error_msg})
