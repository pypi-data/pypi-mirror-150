from paradoxdjango.apps import AppConfig
from paradoxdjango.utils.translation import gettext_lazy as _


class SessionsConfig(AppConfig):
    name = "paradoxdjango.contrib.sessions"
    verbose_name = _("Sessions")
