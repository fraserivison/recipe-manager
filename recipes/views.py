from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def test_view(request):
    return render(request, 'registration/test.html')

def index(request):
    print("Index view accessed")
    return HttpResponse("This is Sizzle!")
