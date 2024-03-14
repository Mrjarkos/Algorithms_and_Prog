from django.views.generic import (TemplateView,
                                  ListView,
                                  DetailView)
from .models import Blog
from .forms import BlogForm
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect

class AboutPageView(TemplateView):
    template_name = "about.html"

class BlogPageView(ListView):
    model = Blog
    template_name = "blog.html"

class BlogDetailView(DetailView):
    model = Blog
    template_name = "post_detail.html"

def blog_list(request):
    posts = Blog.objects.all()
    return render(request, BlogPageView.template_name, {'posts': posts})
