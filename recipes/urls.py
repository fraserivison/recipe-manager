from django.urls import path
from .views import LoginView, SignupView, recipe_detail, recipe_list
from allauth.account.views import LogoutView
from . import views

urlpatterns = [
    path('', views.index, name='index'), # Home page
    path('recipes/', recipe_list, name='recipe_list'),  # Recipes list page
    path('recipe/<slug:slug>/', views.recipe_detail, name='recipe_detail'), # Recipe detail page
    path('accounts/login/', LoginView.as_view(), name='account_login'), # Login page
    path('accounts/signup/', SignupView.as_view(), name='account_signup'), # Signup page
    path('accounts/logout/', LogoutView.as_view(), name='account_logout'), # Logout page
    ]