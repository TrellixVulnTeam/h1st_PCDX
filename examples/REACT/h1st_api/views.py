from django.http import HttpResponse

def default(request):
    text = '<HTML><BODY><CENTER><H1>Congratulations! This is your Human-First REST API!</H1></CENTER></BODY></HTML>'
    return HttpResponse(text)
