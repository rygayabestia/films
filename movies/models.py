from django.db import models

class Movie(models.Model):
    movie_id = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.movie_id)