from django.http import HttpResponse

class HttpResponseNoContent(HttpResponse):
    status_code = 204

    def __init__(self):
        HttpResponse.__init__(self)

def profile(request):
    return HttpResponseNoContent()
