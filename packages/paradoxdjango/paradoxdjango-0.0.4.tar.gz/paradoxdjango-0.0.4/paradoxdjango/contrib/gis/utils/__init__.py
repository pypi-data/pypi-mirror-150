"""
 This module contains useful utilities for GeoDjango.
"""
from paradoxdjango.contrib.gis.utils.ogrinfo import ogrinfo  # NOQA
from paradoxdjango.contrib.gis.utils.ogrinspect import mapping, ogrinspect  # NOQA
from paradoxdjango.contrib.gis.utils.srs import add_srs_entry  # NOQA
from paradoxdjango.core.exceptions import ImproperlyConfigured

try:
    # LayerMapping requires DJANGO_SETTINGS_MODULE to be set,
    # and ImproperlyConfigured is raised if that's not the case.
    from paradoxdjango.contrib.gis.utils.layermapping import (  # NOQA
        LayerMapError,
        LayerMapping,
    )
except ImproperlyConfigured:
    pass
