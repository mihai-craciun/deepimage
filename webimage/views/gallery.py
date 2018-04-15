from django.shortcuts import render
from django.views.generic import View
from ..models import User, Album, Photo, PhotoTag, Tag
from .models.userview import user_albums_rank, user_photos_rank, user_tags_rank


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
        profile = User.objects.get(username=user)
        context = {'profile': profile}
        return render(request, 'webimage/gallery/user.html',
                      RenderObject.create(Fields.Users, True, context))


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
