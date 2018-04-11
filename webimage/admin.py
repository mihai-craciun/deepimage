from django.contrib import admin
from webimage.models import Photo, PhotoTag, Album, Tag

# Register your models here.
admin.site.register(Album)
admin.site.register(Photo)
admin.site.register(PhotoTag)
admin.site.register(Tag)