from paradoxdjango.contrib.admindocs.middleware import XViewMiddleware
from paradoxdjango.http import HttpResponse
from paradoxdjango.utils.decorators import decorator_from_middleware
from paradoxdjango.views.generic import View

xview_dec = decorator_from_middleware(XViewMiddleware)


def xview(request):
    return HttpResponse()


class XViewClass(View):
    def get(self, request):
        return HttpResponse()


class XViewCallableObject(View):
    def __call__(self, request):
        return HttpResponse()
