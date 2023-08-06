from paradoxdjango.apps import AppConfig
from paradoxdjango.utils.translation import gettext_lazy as _


class SyndicationConfig(AppConfig):
    name = "paradoxdjango.contrib.syndication"
    verbose_name = _("Syndication")
