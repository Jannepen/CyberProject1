
from django.http import HttpResponse

def fakeLogoutView(request):
    return HttpResponse("You have successfully logged out.")