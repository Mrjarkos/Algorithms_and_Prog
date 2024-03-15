from django.contrib import messages
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout

class LoginPageView(TemplateView):
    template_name = "login.html"

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login:login")
    template_name = "registration/signup.html"

def logout_view(request):
  logout(request)
  response = redirect('/')
  return response
