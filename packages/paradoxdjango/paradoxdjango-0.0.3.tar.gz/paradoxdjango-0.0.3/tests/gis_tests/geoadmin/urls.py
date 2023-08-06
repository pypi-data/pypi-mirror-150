from paradoxdjango.contrib import admin
from paradoxdjango.urls import include, path

urlpatterns = [
    path("admin/", include(admin.site.urls)),
]
