# Generated by Django 4.2.16 on 2024-09-29 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_remove_recipe_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
