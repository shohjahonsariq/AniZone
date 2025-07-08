from django.db import models
from django.contrib.auth.models import User
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.URLField(blank=True, null=True)

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Anime(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='anime_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_animes', blank=True)
    views = models.PositiveIntegerField(default=0)
    categories = models.ManyToManyField(Category, related_name='animes', blank=True)  # ✅

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

class AnimeView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'anime')  # Har user anime uchun 1 marta yoziladi

    def __str__(self):
        return f"{self.user.username} -> {self.anime.title}"

class Comment(models.Model):
    anime = models.ForeignKey(Anime, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} izoh qoldirdi'
    
class Episode(models.Model):
    anime = models.ForeignKey(Anime, related_name='episodes', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    video_url = models.URLField()
    episode_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.anime.title} - Ep {self.episode_number}"
