from django.shortcuts import render
from django.http import HttpResponse
from allauth.account.views import LoginView as AllauthLoginView, SignupView as AllauthSignupView, LogoutView as AllauthLogoutView

# Create your views here.
def index(request):
    return render(request, 'index.html')

class LoginView(AllauthLoginView):
    template_name = 'account/login.html'

class SignupView(AllauthSignupView):
    template_name = 'account/signup.html'

class LogoutView(AllauthLogoutView):
    template_name = 'account/logout.html'