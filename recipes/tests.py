from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Recipe
from .forms import RecipeForm
from unittest.mock import patch 

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
        self.assertEqual(form.cleaned_data['title'], 'Test Recipe')
    
    def test_invalid_recipe_form(self):
        form_data = {
            'title': 'A'*36,  # Too long
            'description': 'Too long description exceeding limit'*10,
            'ingredients': '',  # Missing ingredients
            'instructions': '',  # Missing instructions
            'cooking_time': -10,  # Invalid cooking time
            'servings': -1,  # Invalid servings
            'category': '',  # Missing category
            'status': 1, # Published
        }
        form = RecipeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertIn('ingredients', form.errors)
        self.assertIn('instructions', form.errors)
        self.assertIn('category', form.errors)

class SlugGenerationTests(TestCase):
    @patch('cloudinary.uploader.upload')
    def test_slug_is_created_on_save(self, mock_upload):
        mock_upload.return_value = {
            'secure_url': 'http://example.com/fake-image.jpg'
        }
        user = User.objects.create(username='testuser')
        recipe = Recipe.objects.create(
            title='Test Recipe',
            author=user,
            description='Test Description',
            cooking_time=20,
            servings=2,
            status=1,
            featured_image='http://example.com/fake-image.jpg'
        )
        self.assertEqual(recipe.slug, 'test-recipe')
        self.assertEqual(recipe.featured_image, 'http://example.com/fake-image.jpg')

class RecipeViewTests(TestCase):
    @patch('cloudinary.CloudinaryResource.url', return_value='mocked_url')
    def setUp(self, mock_url):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    @patch('cloudinary.CloudinaryResource.url', return_value='mocked_url')
    def test_create_recipe_view(self, mock_url):
        response = self.client.get(reverse('create_recipe'))
        self.assertEqual(response.status_code, 200)

    @patch('cloudinary.CloudinaryResource.url', return_value='mocked_url')
    def test_create_recipe_view_redirects_when_not_logged_in(self, mock_url):
        self.client.logout()
        response = self.client.get(reverse('create_recipe'))
        self.assertEqual(response.status_code, 302)    
    
    @patch('cloudinary.CloudinaryResource.url', return_value='mocked_url')
    def test_recipe_list_view_pagination(self, mock_url):
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
        self.assertEqual(len(response.context['page_obj']), 6)

    @patch('cloudinary.CloudinaryResource.url', return_value='mocked_url')
    def test_recipe_detail_view(self, mock_url):
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
            'email': 'newuser@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
        })
        self.assertEqual(response.status_code, 302)

    def test_login_view(self):
        User.objects.create_user(username='testuser', password='password')
        response = self.client.post(reverse('account_login'), {
            'login': 'testuser',
            'password': 'password',
        })
        self.assertEqual(response.status_code, 302)

    def test_access_create_recipe_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('create_recipe'))
        self.assertEqual(response.status_code, 302)