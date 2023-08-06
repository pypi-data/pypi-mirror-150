from paradoxdjango.apps import AppConfig
from paradoxdjango.core import serializers
from paradoxdjango.utils.translation import gettext_lazy as _


class GISConfig(AppConfig):
    default_auto_field = "paradoxdjango.db.models.AutoField"
    name = "paradoxdjango.contrib.gis"
    verbose_name = _("GIS")

    def ready(self):
        serializers.BUILTIN_SERIALIZERS.setdefault(
            "geojson", "paradoxdjango.contrib.gis.serializers.geojson"
        )
