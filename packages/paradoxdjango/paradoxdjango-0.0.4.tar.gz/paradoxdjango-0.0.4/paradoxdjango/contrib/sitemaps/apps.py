from paradoxdjango.apps import AppConfig
from paradoxdjango.utils.translation import gettext_lazy as _


class SiteMapsConfig(AppConfig):
    default_auto_field = "paradoxdjango.db.models.AutoField"
    name = "paradoxdjango.contrib.sitemaps"
    verbose_name = _("Site Maps")
