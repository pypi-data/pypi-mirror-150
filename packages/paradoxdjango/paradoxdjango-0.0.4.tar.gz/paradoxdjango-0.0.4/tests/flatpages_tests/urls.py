from paradoxdjango.contrib.flatpages.sitemaps import FlatPageSitemap
from paradoxdjango.contrib.sitemaps import views
from paradoxdjango.urls import include, path

urlpatterns = [
    path(
        "flatpages/sitemap.xml",
        views.sitemap,
        {"sitemaps": {"flatpages": FlatPageSitemap}},
        name="paradoxdjango.contrib.sitemaps.views.sitemap",
    ),
    path("flatpage_root/", include("paradoxdjango.contrib.flatpages.urls")),
    path("accounts/", include("paradoxdjango.contrib.auth.urls")),
]
