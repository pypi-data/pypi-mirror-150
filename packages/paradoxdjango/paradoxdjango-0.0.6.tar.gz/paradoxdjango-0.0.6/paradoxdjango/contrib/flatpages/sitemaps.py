from paradoxdjango.apps import apps as django_apps
from paradoxdjango.contrib.sitemaps import Sitemap
from paradoxdjango.core.exceptions import ImproperlyConfigured


class FlatPageSitemap(Sitemap):
    def items(self):
        if not django_apps.is_installed("paradoxdjango.contrib.sites"):
            raise ImproperlyConfigured(
                "FlatPageSitemap requires paradoxdjango.contrib.sites, which isn't installed."
            )
        Site = django_apps.get_model("sites.Site")
        current_site = Site.objects.get_current()
        return current_site.flatpage_set.filter(registration_required=False)
