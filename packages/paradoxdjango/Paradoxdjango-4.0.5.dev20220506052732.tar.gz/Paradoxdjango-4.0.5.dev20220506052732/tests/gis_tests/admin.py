try:
    from paradoxdjango.contrib.gis import admin
except ImportError:
    from paradoxdjango.contrib import admin

    admin.GISModelAdmin = admin.ModelAdmin
    # RemovedInDjango50Warning.
    admin.OSMGeoAdmin = admin.ModelAdmin
