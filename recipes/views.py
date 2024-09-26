from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("This is Sizzle!")

def login_view(request):
    return render(request, 'account/login.html')
