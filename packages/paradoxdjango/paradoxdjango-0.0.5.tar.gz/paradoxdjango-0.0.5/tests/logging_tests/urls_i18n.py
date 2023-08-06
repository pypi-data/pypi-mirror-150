from paradoxdjango.conf.urls.i18n import i18n_patterns
from paradoxdjango.http import HttpResponse
from paradoxdjango.urls import path

urlpatterns = i18n_patterns(
    path("exists/", lambda r: HttpResponse()),
)
