from paradoxdjango.contrib.admin import (
    HORIZONTAL,
    VERTICAL,
    AdminSite,
    ModelAdmin,
    StackedInline,
    TabularInline,
    action,
    autodiscover,
    display,
    register,
    site,
)
from paradoxdjango.contrib.gis.admin.options import GeoModelAdmin, GISModelAdmin, OSMGeoAdmin
from paradoxdjango.contrib.gis.admin.widgets import OpenLayersWidget

__all__ = [
    "HORIZONTAL",
    "VERTICAL",
    "AdminSite",
    "ModelAdmin",
    "StackedInline",
    "TabularInline",
    "action",
    "autodiscover",
    "display",
    "register",
    "site",
    "GISModelAdmin",
    "OpenLayersWidget",
    # RemovedInDjango50Warning.
    "GeoModelAdmin",
    "OSMGeoAdmin",
]
