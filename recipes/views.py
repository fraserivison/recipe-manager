from django.shortcuts import render, get_object_or_404
from allauth.account.views import LoginView as AllauthLoginView, SignupView as AllauthSignupView, LogoutView as AllauthLogoutView
from .models import Recipe

# Home page view (no recipes displayed here)
def index(request):
    return render(request, 'index.html')

# Recipes list view (renders the recipes.html template)
def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes.html', {'recipes': recipes})

# Recipe detail view
def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'recipe_detail.html', {'recipe': recipe})    

# Custom login view using allauth
class LoginView(AllauthLoginView):
    template_name = 'account/login.html'

# Custom signup view using allauth
class SignupView(AllauthSignupView):
    template_name = 'account/signup.html'

# Custom logout view using allauth
class LogoutView(AllauthLogoutView):
    template_name = 'account/logout.html'