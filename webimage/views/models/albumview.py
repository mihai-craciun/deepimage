from webimage.models import Photo, Tag
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
