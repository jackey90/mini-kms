import streamlit as st
from utils import api_client
from utils.helpers import format_datetime, status_badge

st.set_page_config(page_title="Integrations — IntelliKnow KMS", page_icon="🔗", layout="wide")
st.title("🔗 Frontend Integration Management")

try:
    integrations = api_client.get_integrations()
except Exception as exc:
    st.error(f"Cannot load integrations: {exc}")
    st.stop()

integration_map = {i["channel"]: i for i in integrations}

# --- Telegram Card ---
st.subheader("📱 Telegram")
tg = integration_map.get("telegram", {})

col1, col2 = st.columns([2, 1])
with col1:
    st.write(f"**Status:** {status_badge(tg.get('status', 'disconnected'))}")
    if tg.get("token_last4"):
        st.write(f"**Token:** ...{tg['token_last4']}")
    if tg.get("last_active_at"):
        st.write(f"**Last active:** {format_datetime(tg['last_active_at'])}")
    if tg.get("error_message"):
        st.error(tg["error_message"])

with col2:
    if st.button("🔌 Test Connection", key="test_telegram"):
        with st.spinner("Testing..."):
            result = api_client.test_integration("telegram")
        if result["success"]:
            st.success(f"✅ {result['message']} ({result['response_time_ms']}ms)")
        else:
            st.error(f"❌ {result['message']}")

with st.expander("⚙️ Configure Telegram"):
    with st.form("telegram_config"):
        token = st.text_input("Bot Token", type="password", placeholder="1234567890:ABCdef...")
        saved = st.form_submit_button("Save Configuration")
    if saved:
        if not token:
            st.warning("Token cannot be empty.")
        else:
            try:
                api_client.configure_telegram(token)
                st.success("✅ Telegram configured successfully!")
                st.rerun()
            except Exception as exc:
                st.error(f"Failed: {exc}")

st.divider()

# --- Teams Card ---
st.subheader("💬 Microsoft Teams")
teams = integration_map.get("teams", {})

col1, col2 = st.columns([2, 1])
with col1:
    st.write(f"**Status:** {status_badge(teams.get('status', 'disconnected'))}")
    if teams.get("token_last4"):
        st.write(f"**App ID:** ...{teams['token_last4']}")
    if teams.get("last_active_at"):
        st.write(f"**Last active:** {format_datetime(teams['last_active_at'])}")
    st.caption("💡 Local testing: Use Bot Framework Emulator → http://localhost:8000/api/integrations/teams/messages")

with col2:
    if st.button("🔌 Test Connection", key="test_teams"):
        with st.spinner("Testing..."):
            result = api_client.test_integration("teams")
        if result["success"]:
            st.success(f"✅ {result['message']}")
        else:
            st.error(f"❌ {result['message']}")

with st.expander("⚙️ Configure Microsoft Teams"):
    with st.form("teams_config"):
        app_id = st.text_input("App ID (from Azure Bot registration)", placeholder="xxxxxxxx-xxxx-...")
        app_pwd = st.text_input("App Password", type="password")
        saved_teams = st.form_submit_button("Save Configuration")
    if saved_teams:
        if not app_id or not app_pwd:
            st.warning("Both App ID and App Password are required.")
        else:
            try:
                api_client.configure_teams(app_id, app_pwd)
                st.success("✅ Teams configured successfully!")
                st.rerun()
            except Exception as exc:
                st.error(f"Failed: {exc}")
