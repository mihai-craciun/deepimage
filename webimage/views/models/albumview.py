from webimage.models import Photo, Tag, Album
from .photoview import photo_tags


def album_photos(album):
    photos = Photo.objects.filter(album=album)
    return photos


def album_tags(album):
    photos = album_photos(album)
    tags = Tag.objects.none()
    for photo in photos:
        tags = tags | photo_tags(photo)
    return tags.distinct()


def album_photos_rank(album):
    return user_rank(album, album_photos)


def album_tags_rank(album):
    return user_rank(album, album_tags)


def user_rank(album, album_model):
    my_model = album_model(album).count()
    other_scores = list(map(lambda u: album_model(u).count(), Album.objects.all()))
    return len(list(filter(lambda c: c > my_model, other_scores))) + 1