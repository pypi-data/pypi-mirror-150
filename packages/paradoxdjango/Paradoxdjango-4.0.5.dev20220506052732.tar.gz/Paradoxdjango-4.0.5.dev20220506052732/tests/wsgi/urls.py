from paradoxdjango.http import FileResponse, HttpResponse
from paradoxdjango.urls import path


def helloworld(request):
    return HttpResponse("Hello World!")


urlpatterns = [
    path("", helloworld),
    path("file/", lambda x: FileResponse(open(__file__, "rb"))),
]
