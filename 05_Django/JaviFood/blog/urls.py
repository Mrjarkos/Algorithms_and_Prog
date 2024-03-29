"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# blog/urls.py
from django.urls import path, include
from .views import (AboutPageView, 
                    BlogPageView, 
                    BlogDetailView, 
                    blog_new,
                    blog_edit,
                    blog_delete)

urlpatterns = [
    path("", BlogPageView.as_view(), name = "home"),
    path("blog/<slug>/", BlogDetailView.as_view(), name = "post_detail"),
    path("new", blog_new, name = "blog_new"),
    path('edit/<slug>/', blog_edit, name='blog_edit'),
    path("about/", AboutPageView.as_view(), name = "about"),
    path('delete/<slug>/', blog_delete, name='blog_delete'),
]
