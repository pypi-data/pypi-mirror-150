from paradoxdjango.conf.urls.i18n import i18n_patterns
from paradoxdjango.http import HttpResponse
from paradoxdjango.urls import path, re_path
from paradoxdjango.utils.translation import gettext_lazy as _

urlpatterns = i18n_patterns(
    re_path(r"^(?P<arg>[\w-]+)-page", lambda request, **arg: HttpResponse(_("Yes"))),
    path("simple/", lambda r: HttpResponse(_("Yes"))),
    re_path(r"^(.+)/(.+)/$", lambda *args: HttpResponse()),
    prefix_default_language=False,
)
