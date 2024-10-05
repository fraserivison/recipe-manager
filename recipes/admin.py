from django.contrib import admin
from .models import Recipe
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
class RecipeAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ['title']
    list_filter = ()
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('description', 'ingredients', 'instructions')

admin.site.register(Recipe, RecipeAdmin)