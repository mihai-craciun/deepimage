from django.http import Http404
from django.shortcuts import render
from django.views.generic import View
from ..models import User, Album, Photo, PhotoTag, Tag
from .models.userview import user_albums_rank, user_photos_rank, user_tags_rank, user_tags, user_albums, user_photos
from .models.albumview import album_photos, album_tags


class Fields:
    Tags = 'Tags'
    Users = 'Users'


class RenderObject:
    class Title:
        Tags = 'Gallery - Tags'
        Users = 'Gallery - Users'

    @staticmethod
    def create(field_type, multiple, context=None):
        obj = {}
        if field_type == Fields.Tags:
            obj['title'] = RenderObject.Title.Tags
            obj['field'] = Fields.Tags
        elif field_type == Fields.Users:
            obj['title'] = RenderObject.Title.Users
            obj['field'] = Fields.Users
        if multiple:
            obj['gallery_mode'] = True
        else:
            obj['gallery_mode'] = False
        if context is not None:
            obj.update(context)
        return obj


class UsersView(View):
    def get(self, request):
        userstring = request.GET.get('userstring', None)
        users = UsersView.filter(userstring)
        users = list(map(lambda u: {
            'user': u,
            'albums': user_albums_rank(u),
            'photos': user_photos_rank(u),
            'tags': user_tags_rank(u),
        }, users))
        context = {
            'users': users,
            'filter': userstring,
        }
        return render(request, 'webimage/gallery/users.html',
                      RenderObject.create(Fields.Users, True, context))

    @staticmethod
    def filter(userstring):
        if userstring is None:
            return User.objects.all()
        username_search = User.objects.all().filter(username__icontains=userstring)
        first_name_search = User.objects.all().filter(first_name__icontains=userstring)
        last_name_search = User.objects.all().filter(last_name__icontains=userstring)
        return username_search | first_name_search | last_name_search


class UserView(View):
    def get(self, request, user):
        profile = UserView.get_profile_or_404(user)
        tags = user_tags(profile)
        albums = user_albums(profile)
        context = {
            'profile': profile,
            'albums_count': albums.count(),
            'albums_rank': user_albums_rank(profile),
            'photos_count': user_photos(profile).count(),
            'photos_rank': user_photos_rank(profile),
            'tags_count': tags.count(),
            'tags_rank': user_tags_rank(profile),
            'tags_list': tags[:5],
            'albums': list(map(lambda album: {
                'album': album,
                'photos': album_photos(album).count(),
                'tags': album_tags(album).count(),
            }, albums))
        }
        return render(request, 'webimage/gallery/user.html',
                      RenderObject.create(Fields.Users, True, context))

    @staticmethod
    def get_profile_or_404(user):
        try:
            profile = User.objects.get(username=user)
            return profile
        except User.DoesNotExist:
            raise Http404("The profile you're trying to access does not exist")


class AlbumView(View):
    def get(self, request, user, album):
        return render(request, 'webimage/gallery/album.html',
                      RenderObject.create(Fields.Users, True))


class PhotoView(View):
    def get(self, request, user, album, photo):
        return render(request, 'webimage/gallery/album.html',
                      RenderObject.create(Fields.Users, False))


class TagsView(View):
    def get(self, request):
        return render(request, 'webimage/gallery/tags.html',
                      RenderObject.create(Fields.Tags, True))


class TagView(View):
    def get(self, request, tag):
        return render(request, 'webimage/gallery/tag.html',
                      RenderObject.create(Fields.Tags, False))
