from django import forms
from .models import Recipe

CATEGORY_CHOICES = [
    ('Appetiser', 'Appetiser'),
    ('Main Course', 'Main Course'),
    ('Dessert', 'Dessert'),
    ('Soup', 'Soup'),
    ('Salad', 'Salad'),
    ('Snack', 'Snack'),
    ('Breakfast', 'Breakfast'),
    ('Brunch', 'Brunch'),
    ('Baking', 'Baking'),
    ('Beverage', 'Beverage'),
    ('Side Dish', 'Side Dish'),
    ('Vegetarian', 'Vegetarian'),
    ('Vegan', 'Vegan'),
    ('Gluten-Free', 'Gluten-Free'),
    ('Pasta', 'Pasta'),
    ('Rice', 'Rice'),
    ('Grilled', 'Grilled'),
    ('Tray Bake', 'Tray Bake'),
    ('Stir-Fry', 'Stir-Fry'),
    ('Slow Cooker', 'Slow Cooker'),
    ('Seafood', 'Seafood'),
    ('Ethnic Cuisine', 'Ethnic Cuisine'),
]

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title',
            'featured_image',
            'description',
            'ingredients',
            'instructions',
            'cooking_time',
            'servings',
            'category',
            'status'
        ]
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 1,
                'style': 'resize: none;',
                'placeholder': 'Enter a brief description...',
                'maxlength': '45'
            }),
            'title': forms.TextInput(attrs={
                'placeholder': 'Recipe Title',
            }),
            'ingredients': forms.Textarea(attrs={
                'placeholder': 'List ingredients (one per line)',
            }),
            'instructions': forms.Textarea(attrs={
                'placeholder': 'Enter step-by-step instructions (one step per line)',
            }),
            'cooking_time': forms.NumberInput(attrs={
                'placeholder': 'Cooking time (in minutes)',
            }),
            'servings': forms.NumberInput(attrs={
                'placeholder': 'Number of servings',
            }),
            'category': forms.Select(choices=CATEGORY_CHOICES),
            }

        title = forms.CharField(help_text='Enter the title of the recipe.')
        description = forms.CharField(help_text='Enter a brief description of the recipe, less than 45 characters.')
        ingredients = forms.CharField(help_text='List each ingredient on a new line, e.g.,\n- Ingredient 1\n- Ingredient 2.')
        instructions = forms.CharField(help_text='List each step of the cooking process on a new line- numbers will show up automatically e.g.,\n Preheat the oven.\n Mix ingredients.')
        cooking_time = forms.IntegerField(help_text='Enter the cooking time in minutes.')
        servings = forms.IntegerField(help_text='Enter the number of servings the recipe makes.')
        category = forms.ChoiceField(help_text='Select a category for the recipe.')

def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) > 45:
            raise forms.ValidationError('Description must be at least less than 45 characters long.')
        return description