from django.db import models
from movies.models import Movie  # Убедитесь, что модель Movie существует
#from users.models import User

class User(models.Model):
    name = models.CharField(max_length=255)
    login = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Liked(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')  # Уникальная пара пользователь-фильм

    def __str__(self):
        return f'{self.user.name} likes {self.movie.title}'