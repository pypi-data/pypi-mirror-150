from paradoxdjango.conf.urls.i18n import i18n_patterns
from paradoxdjango.urls import path
from paradoxdjango.views.generic import TemplateView

view = TemplateView.as_view(template_name="dummy.html")

urlpatterns = i18n_patterns(
    path("prefixed/", view, name="prefixed"),
)
