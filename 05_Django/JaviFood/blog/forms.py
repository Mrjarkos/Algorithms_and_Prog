from django.forms import ModelForm

from .models import Blog, User

class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'summary', 'post', 'slug', 'cover', 'author']
        
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'rol']