from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=100)
    summary = models.CharField(max_length=255)
    content = models.TextField()
    slug = models.SlugField(unique=True)
    cover = models.URLField()
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-added']

    def __str__(self):
        return self.title
