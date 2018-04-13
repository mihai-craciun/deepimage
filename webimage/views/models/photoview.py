from webimage.models import PhotoTag, Tag


def photo_tags(photo):
    phototags = PhotoTag.objects.filter(photo=photo)
    tags = Tag.objects.filter(phototag__in=phototags)
    return tags

