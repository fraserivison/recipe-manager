from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from allauth.account.views import LoginView as AllauthLoginView, SignupView as AllauthSignupView, LogoutView as AllauthLogoutView
from .models import Recipe

# Create your views here.
def index(request):
    recipes = Recipe.objects.all()
    return render(request, 'index.html', {'recipes': recipes})

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'recipe_detail.html', {'recipe': recipe})    

class LoginView(AllauthLoginView):
    template_name = 'account/login.html'

class SignupView(AllauthSignupView):
    template_name = 'account/signup.html'

class LogoutView(AllauthLogoutView):
    template_name = 'account/logout.html'