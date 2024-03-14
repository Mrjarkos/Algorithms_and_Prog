from django.contrib import messages
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout

class LoginPageView(TemplateView):
    template_name = "login.html"

def logout_view(request):
  logout(request)
  response = redirect('/')
  return response
