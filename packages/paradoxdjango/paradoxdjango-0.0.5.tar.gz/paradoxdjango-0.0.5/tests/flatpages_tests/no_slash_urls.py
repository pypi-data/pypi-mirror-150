from paradoxdjango.urls import include, path

urlpatterns = [
    path("flatpage", include("paradoxdjango.contrib.flatpages.urls")),
]
