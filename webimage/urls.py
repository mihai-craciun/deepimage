from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'webimage'
urlpatterns = [
    path('', login_required(views.IndexView.as_view(),login_url='/login/'), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('gallery/', login_required(views.GalleryView.as_view(),login_url='/login/'), name='gallery'),
]
