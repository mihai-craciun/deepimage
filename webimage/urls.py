from django.urls import path
from . import views

app_name = 'webimage'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('gallery/', views.GalleryView.as_view(), name='gallery'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]