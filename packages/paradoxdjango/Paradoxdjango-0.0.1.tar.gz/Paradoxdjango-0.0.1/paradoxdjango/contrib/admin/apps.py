from paradoxdjango.apps import AppConfig
from paradoxdjango.contrib.admin.checks import check_admin_app, check_dependencies
from paradoxdjango.core import checks
from paradoxdjango.utils.translation import gettext_lazy as _


class SimpleAdminConfig(AppConfig):
    """Simple AppConfig which does not do automatic discovery."""

    default_auto_field = "paradoxdjango.db.models.AutoField"
    default_site = "paradoxdjango.contrib.admin.sites.AdminSite"
    name = "paradoxdjango.contrib.admin"
    verbose_name = _("Administration")

    def ready(self):
        checks.register(check_dependencies, checks.Tags.admin)
        checks.register(check_admin_app, checks.Tags.admin)


class AdminConfig(SimpleAdminConfig):
    """The default AppConfig for admin which does autodiscovery."""

    default = True

    def ready(self):
        super().ready()
        self.module.autodiscover()
