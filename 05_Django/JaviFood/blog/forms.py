from django.forms import ModelForm
from django.contrib.auth.models import User

from .models import Blog

class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'summary', 'content', 'slug', 'cover', 'author']