from paradoxdjango.apps import AppConfig
from paradoxdjango.utils.translation import gettext_lazy as _


class MessagesConfig(AppConfig):
    name = "paradoxdjango.contrib.messages"
    verbose_name = _("Messages")
