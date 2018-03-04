from django.shortcuts import render
from django.views.generic import View
from .forms import *
# Create your views here.

class IndexView(View):
    def get(self, request):
        return render(request, 'webimage/index.html',{
            'title' : 'Home',
        })

class GalleryView(View):
    def get(self, request):
        return render(request, 'webimage/gallery.html', {
            'title' : 'Gallery'
        })

class LoginView(View):
    def get(self, request):
        return render(request, 'webimage/auth/login.html', {
            'title' : 'Login',
            'form' : LoginForm(),
        })

class RegisterView(View):
    def get(self, request):
        return render(request, 'webimage/auth/register.html', {
            'title' : 'Register',
            'form' : RegisterForm(),
        })

class LogoutView(View):
    def post(self, reuqest):
        return None