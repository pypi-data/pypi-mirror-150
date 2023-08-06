from paradoxdjango.http import HttpResponse
from paradoxdjango.utils.decorators import method_decorator
from paradoxdjango.views.decorators.common import no_append_slash
from paradoxdjango.views.generic import View


def empty_view(request, *args, **kwargs):
    return HttpResponse()


@no_append_slash
def sensitive_fbv(request, *args, **kwargs):
    return HttpResponse()


@method_decorator(no_append_slash, name="dispatch")
class SensitiveCBV(View):
    def get(self, *args, **kwargs):
        return HttpResponse()
