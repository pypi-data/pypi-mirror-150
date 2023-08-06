from paradoxdjango.contrib.flatpages import views
from paradoxdjango.urls import path

urlpatterns = [
    path("<path:url>", views.flatpage, name="paradoxdjango.contrib.flatpages.views.flatpage"),
]
