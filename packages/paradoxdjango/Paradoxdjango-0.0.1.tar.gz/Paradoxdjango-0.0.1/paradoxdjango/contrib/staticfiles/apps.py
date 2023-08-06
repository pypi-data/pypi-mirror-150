from paradoxdjango.apps import AppConfig
from paradoxdjango.contrib.staticfiles.checks import check_finders
from paradoxdjango.core import checks
from paradoxdjango.utils.translation import gettext_lazy as _


class StaticFilesConfig(AppConfig):
    name = "paradoxdjango.contrib.staticfiles"
    verbose_name = _("Static Files")
    ignore_patterns = ["CVS", ".*", "*~"]

    def ready(self):
        checks.register(check_finders, checks.Tags.staticfiles)
