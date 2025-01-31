from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from allauth.account.views import LoginView as AllauthLoginView, \
    SignupView as AllauthSignupView, LogoutView as AllauthLogoutView
from .models import Recipe  # Rating (comment out for now)
from .forms import RecipeForm, RatingForm
from django.utils.text import slugify
import uuid


# Home page view (no recipes displayed here)
def index(request):
    return render(request, 'index.html')


# Recipes list view (renders the recipes.html template)
def recipe_list(request):
    search_query = request.GET.get('search', '')

    if search_query:
        recipes = Recipe.objects.filter(title__icontains=search_query)
    else:
        recipes = Recipe.objects.all()

    paginator = Paginator(recipes, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'recipes.html',
        {'page_obj': page_obj, 'search_query': search_query}
    )


# Recipe detail view
def recipe_detail(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)

    existing_rating = None
    if request.user.is_authenticated:
        existing_rating = recipe.ratings.filter(user=request.user).first()

    if request.method == 'POST':
        if request.user.is_authenticated:
            rating_form = RatingForm(request.POST)
            if rating_form.is_valid():
                if existing_rating:
                    # Update the existing rating
                    existing_rating.score = rating_form.cleaned_data['score']
                    existing_rating.save()
                    messages.success(
                        request,
                        'Your rating has been updated!'
                    )
                else:
                    # Save the new rating
                    rating = rating_form.save(commit=False)
                    rating.recipe = recipe
                    rating.user = request.user
                    rating.save()
                    messages.success(
                        request,
                        'Your rating has been submitted!'
                    )

                # Update the average rating for the recipe
                recipe.update_average_rating()
                return redirect('recipe_detail', slug=slug)
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            messages.error(
                request,
                'You need to be logged in to rate this recipe.'
            )
            rating_form = RatingForm()
    else:
        rating_form = RatingForm()

    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'rating_form': rating_form,
        'existing_rating': existing_rating,
    })


# Create a recipe
@login_required
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            unique_slug = slugify(recipe.title)
            while Recipe.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{slugify(recipe.title)}-{uuid.uuid4().hex[:6]}"
            recipe.slug = unique_slug
            recipe.save()
            messages.success(request, 'Recipe added successfully!')
            return redirect('recipe_list')
    else:
        form = RecipeForm()
    return render(request, 'recipes/create_recipe.html', {'form': form})


# Recipe edit view
@login_required
def edit_recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)

    # Check if the user is the author or an admin
    if recipe.author != request.user and not request.user.is_staff:
        messages.error(
            request,
            'You do not have permission to edit this recipe.'
        )
        return redirect('recipe_detail', slug=slug)

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, 'Recipe updated successfully!')
            return redirect('recipe_detail', slug=recipe.slug)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RecipeForm(instance=recipe)

    return render(request, 'recipes/edit_recipe.html', {
        'form': form,
        'recipe': recipe,
        'title': 'Edit Recipe',
    })


# Recipe delete view
@login_required
def delete_recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)

    # Check if the user is the author or an admin
    if recipe.author != request.user and not request.user.is_staff:
        messages.error(
            request,
            'You do not have permission to delete this recipe.'
        )
        return redirect('recipe_detail', slug=slug)

    if request.method == 'POST':
        recipe.delete()
        messages.success(request, 'Recipe deleted successfully!')
        return redirect('recipe_list')

    return render(request, 'recipes/delete_recipe.html', {
        'recipe': recipe,
        'title': 'Delete Recipe',
    })


# Custom login view using allauth
class LoginView(AllauthLoginView):
    template_name = 'account/login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'You have logged in successfully.')
        return response

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', super().get_success_url())


# Custom signup view using allauth
class SignupView(AllauthSignupView):
    template_name = 'account/signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'You have signed up successfully.')
        return response

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', super().get_success_url())


# Custom logout view using allauth
class LogoutView(AllauthLogoutView):
    template_name = 'account/logout.html'

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'You have signed out.')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', super().get_success_url())


# Custom 404 view
def custom_404_view(request, exception):
    return render(request, '404.html', status=404)
