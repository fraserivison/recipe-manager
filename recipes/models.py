from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.utils.text import slugify

# Create your models here.
class Recipe(models.Model):
    title = models.CharField(max_length=35)
    slug = models.SlugField(max_length=45, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_recipes")
    featured_image = CloudinaryField('image')
    description = models.TextField(max_length=45)
    ingredients = models.TextField(null=True, blank=True)
    instructions = models.TextField()
    cooking_time = models.IntegerField()
    servings = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    average_rating = models.FloatField(default=0)


    # Meta class to define ordering of records
    class Meta:
        ordering = ['-created_on']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def update_average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            total_score = sum(rating.score for rating in ratings)
            average_score = total_score / ratings.count()
            self.average_rating = average_score
        else:
            self.average_rating = 0
        self.save()     

    def __str__(self):
        return f"{self.title} by {self.author}"

class Rating(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    score = models.IntegerField(choices=[
    (1, '1 Star'),
    (2, '2 Stars'),
    (3, '3 Stars'),
    (4, '4 Stars'),
    (5, '5 Stars'),
    ])

    class Meta:
        unique_together = ('recipe', 'user')

    def __str__(self):
        return f"{self.user.username} rated {self.recipe.title} - {self.score}"    