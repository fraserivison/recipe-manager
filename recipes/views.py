from django.shortcuts import render
from django.http import HttpResponse
from allauth.account.views import LoginView as AllauthLoginView, SignupView as AllauthSignupView

# Create your views here.
class LoginView(AllauthLoginView):
    template_name = 'account/login.html'

class SignupView(AllauthSignupView):
    template_name = 'account/signup.html'

def index(request):
    return HttpResponse("This is Sizzle!")