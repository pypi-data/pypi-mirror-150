from paradoxdjango.contrib.sitemaps import views
from paradoxdjango.urls import path

from .http import simple_sitemaps

urlpatterns = [
    path(
        "simple/index.xml",
        views.index,
        {"sitemaps": simple_sitemaps},
        name="paradoxdjango.contrib.sitemaps.views.index",
    ),
]
