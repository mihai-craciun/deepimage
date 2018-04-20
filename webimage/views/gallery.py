from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views.generic import View
from ..models import User, Album, Photo, PhotoTag, Tag
from ..forms import AlbumForm, ImagesForm
from .models.userview import user_albums_rank, user_photos_rank, user_tags_rank, user_tags, user_albums, user_photos
from .models.albumview import album_photos, album_tags, album_photos_rank, album_tags_rank
from .models.photoview import photo_tags
from .models.tagview import tag_phototags


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

        if user != request.user.username:
            albums = albums.filter(private=False)

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
        user = UserView.get_profile_or_404(user)
        album = AlbumView.get_album_or_404(album)
        photos = album_photos(album)
        tags = album_tags(album)
        form = ImagesForm()

        if album.user != user:
            raise Http404("Album does not exist")
        if album.private and user != request.user:
            raise Http404("Album does not exist")

        context = {
            'profile': user,
            'album': album,
            'photos_count': album_photos(album).count(),
            'photos_rank': album_photos_rank(album),
            'tags_count': tags.count(),
            'tags_rank': album_tags_rank(album),
            'tags_list': tags,
            'form': form,
            'photos': list(map(lambda photo: {
                'photo': photo,
                'tags': photo_tags(photo)[:5]
            }, photos))
        }
        return render(request, 'webimage/gallery/album.html',
                      RenderObject.create(Fields.Users, True, context))

    @staticmethod
    def get_album_or_404(album):
        try:
            album = Album.objects.get(uuid=album)
            return album
        except Album.DoesNotExist:
            raise Http404("The album you're trying to acces does not exist")


class AlbumDeleteView(View):
    def post(self, request, album):
        album = AlbumView.get_album_or_404(album)
        if album.user.username != request.user.username:
            return HttpResponseForbidden()
        album.delete()
        return redirect('webimage:gallery_user', request.user.username)


class AlbumAddView(View):
    def get(self, request):
        form = AlbumForm()
        context = {
            'form': form
        }
        return render(request, 'webimage/gallery/album_add.html',
                      RenderObject.create(Fields.Users, False, context))

    def post(self, request):
        form = AlbumForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            # Check if album exists
            album = Album.objects.filter(user=request.user).filter(name=data['name'])

            if len(album) == 0:
                album = Album.objects.create(user=request.user, name=data['name'], private=data['private'])
                return redirect('webimage:gallery_user_album', request.user.username, album.uuid)
            else:
                form.add_error('name', 'You already have an album with this name')
                context = {'form': form}
                return render(request, 'webimage/gallery/album_add.html',
                              RenderObject.create(Fields.Users, False, context))


class AlbumEditView(View):
    def get(self, request, album):

        album = AlbumView.get_album_or_404(album)
        if album.user != request.user:
            return HttpResponseForbidden()

        form = AlbumForm(initial={
            'name': album.name,
            'private': album.private
        })

        context = {
            'album': album,
            'form': form
        }
        return render(request, 'webimage/gallery/album_edit.html',
                      RenderObject.create(Fields.Users, False, context))

    def post(self, request, album):

        album = AlbumView.get_album_or_404(album)
        if album.user != request.user:
            return HttpResponseForbidden()

        form = AlbumForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            # Check if album exists
            name_album = Album.objects.filter(user=request.user).filter(name=data['name'])

            if len(name_album) == 0 or (len(name_album) == 1 and name_album[0].uuid == album.uuid):
                album.name = data['name']
                album.private = data['private']
                album.save()
                return redirect('webimage:gallery_user_album', request.user.username, album.uuid)
            else:
                form.add_error('name', 'You already have an album with this name')
                context = {'form': form}
                return render(request, 'webimage/gallery/album_edit.html',
                              RenderObject.create(Fields.Users, False, context))


class PhotoView(View):
    def get(self, request, user, album, photo):
        return render(request, 'webimage/gallery/album.html',
                      RenderObject.create(Fields.Users, False))


class PhotoAddView(View):
    def post(self, request, album):
        album = AlbumView.get_album_or_404(album)
        if album.user != request.user:
            return HttpResponseForbidden()

        form = ImagesForm(request.POST, request.FILES)

        if form.is_valid():
            for image in request.FILES.getlist('images'):
                photo = Photo.objects.create(photo=image, album=album)
                photo.save()
        return redirect('webimage:gallery_user_album', request.user, album.uuid)


class TagsView(View):
    def get(self, request):
        tagstring = request.GET.get('tagstring', None)
        tags = TagsView.filter(tagstring)
        tags = list(map(lambda tag: {
            'tag': tag,
            'usages': tag_phototags(tag).count()
        }, tags))
        tags = sorted(tags, key=lambda t: t['usages'], reverse=True)
        context = {
            'tags': tags,
            'filter': tagstring,
        }
        return render(request, 'webimage/gallery/tags.html',
                      RenderObject.create(Fields.Tags, True, context))

    @staticmethod
    def filter(tagstring):
        if tagstring is None:
            return Tag.objects.all()
        else:
            return Tag.objects.filter(tag__icontains=tagstring)


class TagView(View):
    def get(self, request, tag):
        tag = TagView.get_tag_or_404(tag)
        context = {
            'tag': tag,
        }
        return render(request, 'webimage/gallery/tag.html',
                      RenderObject.create(Fields.Tags, False, context))

    @staticmethod
    def get_tag_or_404(tag):
        try:
            tag = Tag.objects.get(tag=tag)
            return tag
        except Tag.DoesNotExist:
            raise Http404("The tag you're trying to access does not exist")
