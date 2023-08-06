from paradoxdjango.apps import AppConfig
from paradoxdjango.utils.translation import gettext_lazy as _


class AdminDocsConfig(AppConfig):
    name = "paradoxdjango.contrib.admindocs"
    verbose_name = _("Administrative Documentation")
