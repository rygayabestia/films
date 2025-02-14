from django.db import models
from movies.models import Movie

class User(models.Model):
    name = models.CharField(max_length=255)
    login = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    liked_movies = models.ManyToManyField(Movie, blank=True)

    def __str__(self):
        return self.name