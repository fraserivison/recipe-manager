from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Recipe
from .forms import RecipeForm

class RecipeFormTests(TestCase):
    def test_valid_recipe_form(self):
        form_data = {
            'title': 'Test Recipe',
            'description': 'Delicious and easy.',
            'ingredients': 'Test ingredients',
            'instructions': 'Test instructions',
            'cooking_time': 30,
            'servings': 4,
            'category': 'Main Course',
            'status': 1
        }
        form = RecipeForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_recipe_form(self):
        form_data = {
            'title': 'A'*36,  # Too long
            'description': 'Too long description exceeding limit'*10,
            'cooking_time': -10,  # Invalid cooking time
            'servings': -1,  # Invalid servings
        }
        form = RecipeForm(data=form_data)
        self.assertFalse(form.is_valid())

class SlugGenerationTests(TestCase):
    def test_slug_is_created_on_save(self):
        user = User.objects.create(username='testuser')
        recipe = Recipe.objects.create(
            title='Test Recipe',
            author=user,
            description='Test Description',
            cooking_time=20,
            servings=2,
            status=1
        )
        self.assertEqual(recipe.slug, 'test-recipe')

class RecipeViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_create_recipe_view(self):
        response = self.client.get(reverse('create_recipe'))
        self.assertEqual(response.status_code, 200)
    
    def test_recipe_list_view_pagination(self):
        for i in range(15):
            Recipe.objects.create(
                title=f'Recipe {i}',
                author=self.user,
                description=f'Test Description {i}',
                cooking_time=20,
                servings=2,
                status=1
            )
        response = self.client.get(reverse('recipe_list') + '?page=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 6)  # Check 6 recipes per page

    def test_recipe_detail_view(self):
        recipe = Recipe.objects.create(
            title='Recipe Detail Test',
            author=self.user,
            description='Test Description',
            cooking_time=20,
            servings=2,
            status=1
        )
        response = self.client.get(reverse('recipe_detail', kwargs={'slug': recipe.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Recipe Detail Test')

class AuthTests(TestCase):
    def test_signup_view(self):
        response = self.client.post(reverse('account_signup'), {
            'username': 'newuser',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
        })
        self.assertEqual(response.status_code, 302)  # Redirects after successful signup

    def test_login_view(self):
        User.objects.create_user(username='testuser', password='password')
        response = self.client.post(reverse('account_login'), {
            'login': 'testuser',
            'password': 'password',
        })
        self.assertEqual(response.status_code, 302)  # Redirects after successful login

    def test_access_create_recipe_requires_login(self):
        response = self.client.get(reverse('create_recipe'))
        self.assertEqual(response.status_code, 302)  # Redirects to login page if not logged in
