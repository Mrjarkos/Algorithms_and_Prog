from django.db import models

class User(models.Model):
    ROL_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    rol = models.CharField(max_length=10, choices=ROL_CHOICES)

    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=100)
    summary = models.CharField(max_length=255)
    post = models.TextField()
    slug = models.SlugField()
    cover = models.URLField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-added']

    def __str__(self):
        return self.title
