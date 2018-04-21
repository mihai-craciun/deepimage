from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import views, gallery
from django.conf.urls.static import static
from django.conf import settings


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
    path('albums/add', auth_required(gallery.AlbumAddView), name='album_add'),
    path('albums/<uuid:album>/delete', auth_required(gallery.AlbumDeleteView), name='album_delete'),
    path('albums/<uuid:album>/edit', auth_required(gallery.AlbumEditView), name='album_edit'),
    path('albums/<uuid:album>/add', auth_required(gallery.PhotoAddView), name='photo_add'),
    path('albums/<uuid:album>/<uuid:photo>/delete', auth_required(gallery.PhotoDeleteView), name='photo_delete'),
    path('albums/<uuid:album>/<uuid:photo>/tag', auth_required(gallery.PhotoTaggingView), name='photo_tagging'),
    path('albums/<uuid:album>/<uuid:photo>/<uuid:photo_tag>/delete', auth_required(gallery.PhotoTagDeleteView),
         name='photo_tag_delete'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
