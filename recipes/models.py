from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.utils.text import slugify

# Create your models here.
class Recipe(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_recipes")
    featured_image = CloudinaryField('image', default='placeholder')
    description = models.TextField()
    ingredients = models.TextField(null=True, blank=True)
    instructions = models.TextField()
    cooking_time = models.IntegerField()
    servings = models.IntegerField()
    category = models.CharField(max_length=100, null=True, blank=True)
    average_rating = models.FloatField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    STATUS = ((0, "Draft"), (1, "Published"))
    status = models.IntegerField(choices=STATUS, default=0)

    # Meta class to define ordering of records
    class Meta:
        ordering = ['-created_on']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)    

    def __str__(self):
        return f"{self.title} by {self.author}"