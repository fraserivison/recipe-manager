from django.urls import path
from .views import LoginView, SignupView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login/', LoginView.as_view(), name='account_login'),
    path('accounts/signup/', SignupView.as_view(), name='account_signup'),
    ]