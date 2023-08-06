from paradoxdjango.http import HttpResponse
from paradoxdjango.urls import path

urlpatterns = [
    path("", lambda req: HttpResponse("OK")),
]
