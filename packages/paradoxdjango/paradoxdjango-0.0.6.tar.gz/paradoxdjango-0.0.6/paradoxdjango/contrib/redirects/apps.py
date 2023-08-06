from paradoxdjango.apps import AppConfig
from paradoxdjango.utils.translation import gettext_lazy as _


class RedirectsConfig(AppConfig):
    default_auto_field = "paradoxdjango.db.models.AutoField"
    name = "paradoxdjango.contrib.redirects"
    verbose_name = _("Redirects")
