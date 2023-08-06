from paradoxdjango.contrib.flatpages import views
from paradoxdjango.urls import path

urlpatterns = [
    path("flatpage/", views.flatpage, {"url": "/hardcoded/"}),
]
