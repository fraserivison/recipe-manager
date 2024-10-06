from django import forms
from .models import Recipe, Rating

# CATEGORY_CHOICES = [
   # ('', 'Select a category'),
   # ('Appetiser', 'Appetiser'),
   # ('Main Course', 'Main Course'),
   # ('Dessert', 'Dessert'),
   # ('Soup', 'Soup'),
   # ('Salad', 'Salad'),
   # ('Snack', 'Snack'),
   # ('Breakfast', 'Breakfast'),
   # ('Brunch', 'Brunch'),
   # ('Baking', 'Baking'),
   # ('Beverage', 'Beverage'),
   # ('Side Dish', 'Side Dish'),
   # ('Vegetarian', 'Vegetarian'),
   # ('Vegan', 'Vegan'),
   # ('Gluten-Free', 'Gluten-Free'),
   # ('Pasta', 'Pasta'),
   # ('Rice', 'Rice'),
   # ('Grilled', 'Grilled'),
   # ('Tray Bake', 'Tray Bake'),
   # ('Stir-Fry', 'Stir-Fry'),
   # ('Slow Cooker', 'Slow Cooker'),
   # ('Seafood', 'Seafood'),
   # ('Ethnic Cuisine', 'Ethnic Cuisine'),
#]

class RecipeForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter the name here...', 'class': 'form-control'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 1,
            'style': 'resize: none;',
            'maxlength': '45',
            'placeholder': 'Enter a brief description...',
            'class': 'form-control'
        })
    )
    ingredients = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'List ingredients (one per line)', 'class': 'form-control'})
    )
    instructions = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter step-by-step instructions (one step per line)', 'class': 'form-control'})
    )
    cooking_time = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'Enter a number', 'class': 'form-control'})
    )
    servings = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'Enter a number', 'class': 'form-control'})
    )
    # category = forms.ChoiceField(
        # choices=CATEGORY_CHOICES,
        # widget=forms.Select(attrs={'class': 'form-control'})
    # )

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
            #'category'
            ]

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) > 45:
            raise forms.ValidationError('Description must be less than 45 characters long.')
        return description

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']
        widgets = {
            'score': forms.Select(choices=[
                (1, '1 Star'),
                (2, '2 Stars'),
                (3, '3 Stars'),
                (4, '4 Stars'),
                (5, '5 Stars'),
            ]),
        }