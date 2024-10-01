from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe  # Use the Recipe model
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
                'rows': 1,  # Limits the visible height to one row
                'style': 'resize: none;',  # Prevents resizing the textarea
                'placeholder': 'Enter a brief description...'  # Optional placeholder
            }),
            'title': forms.TextInput(attrs={
                'placeholder': 'Recipe Title',
            }),
            'ingredients': forms.Textarea(attrs={
                'placeholder': 'List ingredients...',
            }),
            'instructions': forms.Textarea(attrs={
                'placeholder': 'Cooking instructions...',
            }),
            'cooking_time': forms.NumberInput(attrs={
                'placeholder': 'Cooking time (in minutes)',
            }),
            'servings': forms.NumberInput(attrs={
                'placeholder': 'Number of servings',
            }),
            'category': forms.TextInput(attrs={
                'placeholder': 'Recipe category',
            }),
        }

def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) < 10:  # Example: Minimum length of 10 characters
            raise forms.ValidationError('Description must be at least 10 characters long.')
        return description