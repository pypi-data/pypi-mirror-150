from paradoxdjango.conf.urls.i18n import i18n_patterns
from paradoxdjango.http import HttpResponse, StreamingHttpResponse
from paradoxdjango.urls import path
from paradoxdjango.utils.translation import gettext_lazy as _

urlpatterns = i18n_patterns(
    path("simple/", lambda r: HttpResponse()),
    path("streaming/", lambda r: StreamingHttpResponse([_("Yes"), "/", _("No")])),
)
