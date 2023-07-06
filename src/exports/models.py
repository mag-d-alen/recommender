from time import strftime
import uuid
from django.db import models
import pathlib
from django.utils import timezone


def export_file_handler(instance, filename):
    today = timezone.now().strftime('%Y-%m-%d')
    fpath = pathlib.Path(filename)
    extension = fpath.suffix
    if hasattr(instance, 'id'):
        new_filename=f'{instance.id}{extension}'
    else:
        new_filename=f'{uuid.uuid4()}{extension}'
    return f'exports/{today}/{new_filename}'
    

# Create your models here.
class  Export(models.Model):
    id = models.UUIDField(primary_key=True, editable=True, default=uuid.uuid4)
    file = models.FileField(upload_to = export_file_handler, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
