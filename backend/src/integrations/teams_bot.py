"""
Microsoft Teams Bot integration.

For local demo testing, use Bot Framework Emulator:
  https://aka.ms/botframework-emulator

The Teams webhook endpoint is registered at:
  POST /api/integrations/teams/messages

This module provides the activity handler class used by that endpoint.
"""
import logging
from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount

logger = logging.getLogger(__name__)


class KMSTeamsBot(ActivityHandler):
    """Teams bot activity handler — message processing is in the API route."""

    async def on_members_added_activity(
        self, members_added: list[ChannelAccount], turn_context: TurnContext
    ) -> None:
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    "👋 Welcome to IntelliKnow KMS! Ask me anything about your company knowledge base."
                )
