import json
from django.core.management.base import BaseCommand
from recipes.models import Recipe

class Command(BaseCommand):
    help = 'Load recipes from JSON file'

    def handle(self, *args, **kwargs):
        with open('recipes_backup.json') as f:
            data = json.load(f)
            for recipe_data in data:
                slug = recipe_data['fields']['slug']
                
                # Try to get the recipe with this slug, or create a new one
                recipe, created = Recipe.objects.get_or_create(
                    slug=slug,
                    defaults={
                        'title': recipe_data['fields']['title'],
                        'author_id': recipe_data['fields']['author'],
                        'featured_image': recipe_data['fields']['featured_image'],
                        'description': recipe_data['fields']['description'],
                        'ingredients': recipe_data['fields']['ingredients'],
                        'instructions': recipe_data['fields']['instructions'],
                        'cooking_time': recipe_data['fields']['cooking_time'],
                        'servings': recipe_data['fields']['servings'],
                        'created_on': recipe_data['fields']['created_on'],
                        'average_rating': recipe_data['fields']['average_rating'],
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f'Successfully loaded recipe "{recipe.title}"'))
                else:
                    self.stdout.write(self.style.WARNING(f'Recipe with slug "{slug}" already exists. Skipping...'))

