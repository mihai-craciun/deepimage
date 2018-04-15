from webimage.models import Tag, PhotoTag


def tag_phototags(tag):
    return PhotoTag.objects.filter(tag=tag)
