from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('recipes.urls')),
    path('summernote/', include('django_summernote.urls')),
    ]

HANDLER404 = 'recipes.views.custom_404_view'
