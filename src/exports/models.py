from time import strftime
import uuid
from django.db import models
import pathlib
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from exports import storages




def export_file_handler(instance, filename):
    today = timezone.now().strftime('%Y-%m-%d')
    fpath = pathlib.Path(filename)
    extension = fpath.suffix
    dtype = instance.type
    if hasattr(instance, 'id'):
        new_filename = f'{instance.id}{extension}'
    else:
        new_filename = f'{uuid.uuid4()}{extension}'
    return f'exports/{dtype}/{today}/{new_filename}'


class ExportDataTypes(models.TextChoices):
    RATINGS =  'ratings','Ratings'
    MOVIES = 'movies', 'Movies'


# Create your models here.
class Export(models.Model):
    id = models.UUIDField(primary_key=True, editable=True, default=uuid.uuid4)
    file = models.FileField(
        upload_to=export_file_handler, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    type = models.CharField(choices=ExportDataTypes.choices,
                            max_length=20, default=ExportDataTypes.RATINGS)
    latest = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        super().save(*args,**kwargs)
        if self.latest and self.file:
            extension= pathlib.Path(self.file.name).suffix
            path = 'exports/{self.type}/latest.{extension}'
            storages.save(path=path,  file_obj=self.file, overwrite=True )
            qs = Export.objects.filter(type = self.typ).exclude(pk=self.pk)
            qs.update(latest=False)
            
                                    