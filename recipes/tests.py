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
        }
        form = RecipeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertIn('ingredients', form.errors)
        self.assertIn('instructions', form.errors)

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
            )
        response = self.client.get(reverse('recipe_list') + '?page=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 9)

    @patch('cloudinary.CloudinaryResource.url', return_value='mocked_url')
    def test_recipe_detail_view(self, mock_url):
        recipe = Recipe.objects.create(
            title='Recipe Detail Test',
            author=self.user,
            description='Test Description',
            cooking_time=20,
            servings=2,
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

# Error Handling for Forms
class RecipeFormErrorTests(TestCase):
    def test_form_missing_required_fields(self):
        form_data = {
            'title': '',  # Missing title
            'description': 'Test Description',
            'cooking_time': 30,
            'servings': 4,
        }
        form = RecipeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)  # Check if error message for title is present
        self.assertIn('instructions', form.errors)  # Check if error message for missing instructions

# Edge Cases for Views
class RecipeEdgeCaseTests(TestCase):
    def test_form_missing_required_fields(self):
        form_data = {
            'title': 'Unique Recipe',
            'description': 'Duplicate Description',
            'ingredients': 'Test Ingredients',
            'instructions': 'Test Instructions',
            'cooking_time': 30,
            'servings': 4,
        }
        form = RecipeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertIn('instructions', form.errors)

# Edge Cases for Views
class RecipeEdgeCaseTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

# Testing Recipe Editing
class RecipeEditTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
    
    @patch('cloudinary.CloudinaryResource.url', return_value='mocked_url')
    def test_edit_recipe_view(self, mock_url):
        recipe = Recipe.objects.create(
            title='Recipe to Edit',
            author=self.user,
            description='Test Description',
            cooking_time=20,
            servings=2,
        )

        edit_data = {
            'title': 'Edited Recipe Title',
            'description': 'Updated Description',
            'ingredients': 'Updated ingredients',
            'instructions': 'Updated instructions',
            'cooking_time': 40,
            'servings': 5,
        }
        response = self.client.post(reverse('edit_recipe', kwargs={'slug': recipe.slug}), data=edit_data)
        self.assertEqual(response.status_code, 302)  # Redirects after successful edit
        
        updated_recipe = Recipe.objects.get(id=recipe.id)
        self.assertEqual(updated_recipe.title, 'Edited Recipe Title')
        self.assertEqual(updated_recipe.description, 'Updated Description')
        self.assertEqual(updated_recipe.ingredients, 'Updated ingredients')
        self.assertEqual(updated_recipe.instructions, 'Updated instructions')
        self.assertEqual(updated_recipe.cooking_time, 40)
        self.assertEqual(updated_recipe.servings, 5)

    @patch('cloudinary.CloudinaryResource.url', return_value='mocked_url')
    def test_edit_recipe_view_invalid_data(self, mock_url):
        recipe = Recipe.objects.create(
            title='Recipe to Edit',
            author=self.user,
            description='Test Description',
            cooking_time=20,
            servings=2,
        )

        invalid_data = {
            'title': '',  # Invalid: title cannot be empty
            'description': 'Updated Description',
            'ingredients': 'Updated ingredients',
            'instructions': 'Updated instructions',
            'cooking_time': 40,
            'servings': 5,
        }

        response = self.client.post(reverse('edit_recipe', kwargs={'slug': recipe.slug}), data=invalid_data)
        self.assertEqual(response.status_code, 200)  # Should stay on the same page if the form is invalid
        self.assertFormError(response, 'form', 'title', 'This field is required.')

    @patch('cloudinary.CloudinaryResource.url', return_value='mocked_url')
    def test_edit_non_existent_recipe(self, mock_url):
        response = self.client.post(reverse('edit_recipe', kwargs={'slug': 'non-existent-slug'}), data={})
        self.assertEqual(response.status_code, 404)  # Should return 404 for non-existent slug

# Testing Recipe Deletion
class RecipeDeleteTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_delete_recipe(self):
        recipe = Recipe.objects.create(
            title='Recipe to Delete',
            author=self.user,
            description='Test Description',
            cooking_time=20,
            servings=2,
        )
        response = self.client.post(reverse('delete_recipe', kwargs={'slug': recipe.slug}))
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())  # Recipe no longer exists

# Pagination Edge Case
class PaginationEdgeCaseTests(TestCase):
    def test_recipe_list_invalid_page(self):
        response = self.client.get(reverse('recipe_list') + '?page=100')  # Non-existent page
        self.assertEqual(response.status_code, 200)  # Should still return 200 with an empty page
        self.assertEqual(len(response.context['page_obj']), 0)  # No items should be present
