from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import views, gallery


def auth_required(view):
    return login_required(view.as_view(), login_url='/login/')


app_name = 'webimage'
urlpatterns = [
    path('', auth_required(views.IndexView), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('gallery/', include([
        path('', auth_required(gallery.UsersView), name='gallery'),
        path('tags/', auth_required(gallery.TagsView), name='gallery_tags'),
        path('tags/<str:tag>/', auth_required(gallery.TagView), name='gallery_tags_tag'),
        path('<str:user>/', auth_required(gallery.UserView), name='gallery_user'),
        path('<str:user>/<uuid:album>/', auth_required(gallery.AlbumView), name='gallery_user_album'),
        path('<str:user>/<uuid:album>/<uuid:photo>/', auth_required(gallery.PhotoView), name='gallery_user_album_photo')
    ])),
]
