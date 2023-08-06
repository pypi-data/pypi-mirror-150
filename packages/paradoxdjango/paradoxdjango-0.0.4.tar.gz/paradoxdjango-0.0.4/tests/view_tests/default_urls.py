from paradoxdjango.contrib import admin
from paradoxdjango.urls import path

urlpatterns = [
    # This is the same as in the default project template
    path("admin/", admin.site.urls),
]
