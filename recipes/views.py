from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from allauth.account.views import LoginView as AllauthLoginView, SignupView as AllauthSignupView, LogoutView as AllauthLogoutView
from .models import Recipe

# Home page view (no recipes displayed here)
def index(request):
    return render(request, 'index.html')

# Recipes list view (renders the recipes.html template)
def recipe_list(request):
    recipes = Recipe.objects.all()
    paginator = Paginator(recipes, 14)  # Show 14 recipes per page
    page_number = request.GET.get('page')  # Get the current page number from the request
    page_obj = paginator.get_page(page_number)  # Get the recipes for the current page

    return render(request, 'recipes.html', {'page_obj': page_obj})

# Recipe detail view
def recipe_detail(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})    

# Custom login view using allauth
class LoginView(AllauthLoginView):
    template_name = 'account/login.html'

# Custom signup view using allauth
class SignupView(AllauthSignupView):
    template_name = 'account/signup.html'

# Custom logout view using allauth
class LogoutView(AllauthLogoutView):
    template_name = 'account/logout.html'