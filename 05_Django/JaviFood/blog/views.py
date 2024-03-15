from django.views.generic import (TemplateView,
                                  ListView,
                                  DetailView,
                                  CreateView)

from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User

from .models import Blog
from .forms import BlogForm

class AboutPageView(TemplateView):
    template_name = "about.html"

class BlogPageView(ListView):
    model = Blog
    template_name = "blog.html"

class BlogDetailView(DetailView):
    model = Blog
    template_name = "post_detail.html"

def blog_new(request):
    admin_user = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        print(request.POST)
        form = BlogForm(request.POST)
        if form.is_valid():
            form.instance.author = admin_user
            form.save()
            messages.success(request, 'Post Creado')
            return redirect('home')
        else:
            messages.error(request, 'No se pudo crear el post. Revise los campos')
    else:
        form = BlogForm()  
    return render(request, 'post_new.html', {'form': form})

def blog_list(request):
    posts = Blog.objects.all()
    return render(request, BlogPageView.template_name, {'posts': posts})
