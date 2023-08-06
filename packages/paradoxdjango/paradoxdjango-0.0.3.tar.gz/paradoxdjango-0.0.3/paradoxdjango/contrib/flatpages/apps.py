from paradoxdjango.apps import AppConfig
from paradoxdjango.utils.translation import gettext_lazy as _


class FlatPagesConfig(AppConfig):
    default_auto_field = "paradoxdjango.db.models.AutoField"
    name = "paradoxdjango.contrib.flatpages"
    verbose_name = _("Flat Pages")
