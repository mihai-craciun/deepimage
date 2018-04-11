from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator
from django.contrib.auth.models import User
from time import strftime


def get_upload_path(instance, filename):
    return '/'.join(
        ['public', instance.album.user.username, str(instance.album.id),
         '{0}_{1}.{2}'.format(strftime('%d%m%Y%H%M%S'), '.'.join(filename.split('.')[:-1]), filename.split('.')[-1])])


# Create your models here.
class Album(models.Model):
    name = models.CharField(max_length=50, validators=[MinLengthValidator(1)])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    private = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Photo(models.Model):
    photo = models.ImageField('Photo', 'photo', upload_to=get_upload_path)
    private = models.BooleanField(default=False)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Tag(models.Model):
    tag = models.CharField(max_length=50,
                           validators=[RegexValidator('^\w+$', 'Tag contains invalid characters'),
                                       MinLengthValidator(1)])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PhotoTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    image = models.ForeignKey(Photo, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
