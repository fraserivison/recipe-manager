from django import forms
from .models import Recipe, Rating

class RecipeForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter the name here...', 'class': 'form-control'})
    )
    description = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'rows': 1,
            'style': 'resize: none;',
            'maxlength': '45',
            'placeholder': 'Enter a brief description...',
            'class': 'form-control'
        })
    )
    ingredients = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'List ingredients (one per line)', 'class': 'form-control'})
    )

    instructions = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'Enter step-by-step instructions (one step per line)', 'class': 'form-control'})
    )

    cooking_time = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter a number', 'class': 'form-control'})
    )

    servings = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter a number', 'class': 'form-control'})
    )

    featured_image = forms.ImageField(
        required=True,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

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
        ]

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']
        widgets = {
            'score': forms.Select(
                choices=[
                ('', 'Select a rating'),
                (1, '1 Star'),
                (2, '2 Stars'),
                (3, '3 Stars'),
                (4, '4 Stars'),
                (5, '5 Stars'),
            ],
                attrs={'class': 'form-control'},
            ),
        }