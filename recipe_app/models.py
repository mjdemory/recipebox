from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=50)
    bio = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite = models.ManyToManyField('Recipe', related_name='favorite', symmetrical=False)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    description = models.TextField()
    time_required = models.CharField(max_length=20)
    instructions = models.TextField()

    def __str__(self):
        return f"{self.title} - by {self.author.name}"
