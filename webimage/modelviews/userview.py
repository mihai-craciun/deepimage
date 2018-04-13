from ..models import Album, Photo, Tag, User
from .albumview import album_photos, album_tags


def user_albums(user):
    albums = Album.objects.filter(user=user)
    return albums


def user_photos(user):
    albums = user_albums(user)
    photos = Photo.objects.none()
    for album in albums:
        photos = photos | album_photos(album)
    return photos


def user_tags(user):
    albums = user_albums(user)
    tags = Tag.objects.none()
    for album in albums:
        tags = tags | album_tags(album)
    return tags.distinct()


def user_albums_rank(user):
    return user_rank(user, user_albums)


def user_photos_rank(user):
    return user_rank(user, user_photos)


def user_tags_rank(user):
    return user_rank(user, user_tags)


def user_rank(user, user_model):
    my_model = user_model(user).count()
    other_scores = list(map(lambda u: user_model(u).count(), User.objects.all()))
    return len(list(filter(lambda c: c > my_model, other_scores))) + 1
