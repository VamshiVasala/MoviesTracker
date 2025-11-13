from django.db import models
from django.contrib.auth.models import User
from pgvector.django import VectorField
from nltk.tokenize import sent_tokenize
from .embedding import generate_embedding
import time
import numpy as np

class Movie(models.Model):
    STATUS_CHOICES = (
    ('watchlist', 'Watchlist'),
    ('watching', 'Watching'),
    ('watched', 'Watched'),
)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)  
    year = models.IntegerField(default=2024)    
    image_url = models.URLField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='select')
    titleEmb = VectorField(dimensions=96, null=True, blank=True)
    genres = models.TextField(blank=True)
    cast = models.TextField(blank=True)


    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.titleEmb is None and self.title:
            self.titleEmb = generate_embedding(self.title)
        super().save(*args, **kwargs)

    
class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(default=0)
    opinion = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    revieEmb = VectorField(dimensions=96, null=True, blank=True) 
    def __str__(self):
        return f"{self.movie.title} - {self.stars}⭐"
    
    
    def save(self, *args, **kwargs):
        if self.opinion:
            sentences = sent_tokenize(self.opinion)
            embeddings = [generate_embedding(s) for s in sentences]
            self.revieEmb = np.mean(embeddings, axis=0)  # average sentence vectors
        super().save(*args, **kwargs)          
            

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True
    )

    def __str__(self):
        return self.user.username
    
class RecommendedMovie(models.Model):
    title = models.CharField(max_length=200)
    year_of_release = models.CharField(max_length=10)
    short_synopsis = models.TextField()
    main_cast = models.TextField()  # comma-separated string
    poster_url = models.URLField(blank=True, null=True)
    recommend_for = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_recommendations')
    created_at = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=200)
    typeOfFilm = models.CharField(max_length=200,null=True, blank=True)
    genre = models.CharField(max_length=200,null=True, blank=True)

    def __str__(self):
        return self.title
    
class Reaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likedMovies = models.ManyToManyField(Movie, related_name='liked_by', blank=True)
    dislikedMovies = models.ManyToManyField(Movie, related_name='disliked_by', blank=True)

    def __str__(self):
        return f"Reactions of {self.user.username}"
