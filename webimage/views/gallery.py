from django.shortcuts import render
from django.views.generic import View


class Fields:
    Tags = 'Tags'
    Users = 'Users'


class Title:
    Tags = 'Gallery - Tags'
    Users = 'Gallery - Users'


class UsersView(View):
    def get(self, request):
        return render(request, 'webimage/gallery/users.html', {
            'title': Title.Users,
            'field': Fields.Users,
        })


class TagsView(View):
    def get(self, request):
        return render(request, 'webimage/gallery/tags.html', {
            'title': Title.Tags,
            'field': Fields.Tags,
        })


class TagView(View):
    def get(self, request, tag):
        return render(request, 'webimage/gallery/tag.html', {
            'title': Title.Tags,
            'field': Fields.Tags,
        })


class UserView(View):
    def get(self, request, user):
        return render(request, 'webimage/gallery/user.html', {
            'title': Title.Users,
            'field': Fields.Users,
        })


class AlbumView(View):
    def get(self, request, user, album):
        return render(request, 'webimage/gallery/album.html', {
            'title': Title.Users,
            'field': Fields.Users,
        })


class PhotoView(View):
    def get(self, request, user, album, photo):
        return render(request, 'webimage/gallery/album.html', {
            'title': Title.Users,
            'field': Fields.Users,
        })
