from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    imageUrl = models.URLField()
    name = models.CharField(max_length=255)
    description = models.TextField()
    age = models.PositiveIntegerField()
    director = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Puntuación de Películas
class MovieRating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0, choices=[(i, i) for i in range(6)])
