import datetime


STATUS_COLORS = {
    "processed": "🟢",
    "processing": "🟡",
    "pending": "⚪",
    "error": "🔴",
    "connected": "🟢",
    "disconnected": "⚪",
    "success": "✅",
    "fallback": "⚠️",
}


def status_badge(status: str) -> str:
    icon = STATUS_COLORS.get(status.lower(), "❓")
    return f"{icon} {status.capitalize()}"


def format_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


def format_datetime(dt_str: str | None) -> str:
    if not dt_str:
        return "—"
    try:
        dt = datetime.datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        return dt.strftime("%b %d %H:%M")
    except Exception:
        return dt_str


def truncate(text: str, max_len: int = 60) -> str:
    return text if len(text) <= max_len else text[:max_len] + "..."
