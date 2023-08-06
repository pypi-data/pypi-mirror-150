from paradoxdjango.apps import AppConfig
from paradoxdjango.contrib.sites.checks import check_site_id
from paradoxdjango.core import checks
from paradoxdjango.db.models.signals import post_migrate
from paradoxdjango.utils.translation import gettext_lazy as _

from .management import create_default_site


class SitesConfig(AppConfig):
    default_auto_field = "paradoxdjango.db.models.AutoField"
    name = "paradoxdjango.contrib.sites"
    verbose_name = _("Sites")

    def ready(self):
        post_migrate.connect(create_default_site, sender=self)
        checks.register(check_site_id, checks.Tags.sites)
