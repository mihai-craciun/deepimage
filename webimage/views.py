from django.shortcuts import render
from django.views.generic import View
from .forms import RegisterForm
# Create your views here.

class IndexView(View):
    def get(self, request):
        return render(request, 'webimage/index.html',{
            'title' : 'Home',
            'form' : RegisterForm(),
        })
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            return render(request, 'webimage/index.html',{
                'title': 'nu bun',
                'form': 'form'
            })
        else:
            return render(request, 'webimage/index.html', {
                'title' : 'bun',
                'form' : RegisterForm(),
            })
