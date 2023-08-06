from paradoxdjango.urls import path

from .admin import site

urlpatterns = [
    path("test_admin/admin/", site.urls),
]
