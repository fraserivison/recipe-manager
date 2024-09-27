from django.urls import path
from .views import LoginView, SignupView, recipe_detail
from allauth.account.views import LogoutView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('accounts/login/', LoginView.as_view(), name='account_login'),
    path('accounts/signup/', SignupView.as_view(), name='account_signup'),
    path('accounts/logout/', LogoutView.as_view(), name='account_logout'),
    ]