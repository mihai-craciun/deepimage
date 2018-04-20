from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator
from django.contrib.auth.models import User
from datetime import datetime
from uuid import uuid4


def get_upload_path(instance, filename):
    return '/'.join(
        [instance.album.user.username, str(instance.album.uuid),
         '{0}.{1}'.format(datetime.utcnow().strftime('%d-%m-%Y_%H-%M-%S.%f'), filename.split('.')[-1])])


# Create your models here.
class UUIDModel(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)

    class Meta:
        abstract = True


class Album(UUIDModel):
    name = models.CharField(max_length=50, validators=[MinLengthValidator(1)])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    private = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name', 'user')


class Photo(UUIDModel):
    photo = models.ImageField('Photo', 'photo', upload_to=get_upload_path)
    private = models.BooleanField(default=False)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Tag(UUIDModel):
    tag = models.CharField(max_length=50,
                           validators=[RegexValidator('^\w+$', 'Tag contains invalid characters'),
                                       MinLengthValidator(1)],
                           unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PhotoTag(UUIDModel):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    score = models.FloatField('Accuracy score', 'score')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('tag', 'photo')
