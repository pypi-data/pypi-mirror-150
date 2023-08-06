from paradoxdjango.contrib.staticfiles import views
from paradoxdjango.urls import re_path

urlpatterns = [
    re_path("^static/(?P<path>.*)$", views.serve),
]
