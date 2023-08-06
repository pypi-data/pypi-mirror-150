import turbo
from turbo.components import UserBroadcastComponent

from medux.common.models import User, Tenant


class MenuItemBadgeComponent(UserBroadcastComponent):
    """A Turbo component that renders a badge for a menu item
    that can be updated via stream.

    You should not use/instantiate this component directly,
    but subclass it and implement the `get_badge_content()` and
    `get_badge_title()` methods.
    """

    template_name = "common/components/menuitem_badge.html"

    # noinspection PyMethodMayBeStatic
    def get_badge_content(self) -> str:
        """Implement this method in subclasses to render content
        in the badge pill."""
        return ""

    # noinspection PyMethodMayBeStatic
    def get_badge_title(self) -> str:
        """Implement this method in subclasses to render content
        in the badge pill hover text."""
        return ""

    def get_context(self):
        return {
            "badge": self.get_badge_content(),
            "title": self.get_badge_title(),
            "component_id": self.__class__.__name__,
        }


# FIXME
class MessagesComponent(UserBroadcastComponent):
    """A TurboComponent that receives messages from the Django messages
    system and streams them to the frontend."""

    template_name = "common/components/message.html"

    def get_context(self):
        return {"id": 0, "title": "sd", "small_text": "small text", "body": "body"}

    def send_message(self, user: User):
        pass


class TenantStream(turbo.ModelStream):
    class Meta:
        model = Tenant
