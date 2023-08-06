from paradoxdjango.apps import AppConfig
from paradoxdjango.utils.translation import gettext_lazy as _


class HumanizeConfig(AppConfig):
    name = "paradoxdjango.contrib.humanize"
    verbose_name = _("Humanize")
