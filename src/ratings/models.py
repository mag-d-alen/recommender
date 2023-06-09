from curses import def_prog_mode
from datetime import datetime
import zoneinfo
from django.utils import timezone
from django.apps import apps
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType 
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.query import QuerySet
from django.db.models import Avg
from django.db.models.signals import post_save

from suggestions.models import Suggestion


# Create your models here.

User = settings.AUTH_USER_MODEL
ISRAEL_TIMEZONE = zoneinfo.ZoneInfo('Asia/Jerusalem')

class RatingChoice(models.IntegerChoices):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    __empty__ = "Rate the film"
    
class RatingQuerySet(models.QuerySet):
    def avg(self):
        return self.aggregate(average=Avg("value")) ["average"] #creates a dict {"avarage": value}
    
    def movies(self):
        ctype = ContentType.objects.get_for_model(apps.get_model('movies', 'Movie')) #to avoid circular import
        return self.filter(active=True, content_type = ctype)

class RatingManager(models.Manager):
    def get_queryset(self):
        return RatingQuerySet(self.model, using=self._db) #return the result of RQS calculation using the standard db
    def avg(self):
        return self.get_queryset().avg()  #call the get_queryset method
    
    
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(blank=True, null=True, choices=RatingChoice.choices)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id= models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id") 
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(default=timezone.now)
    active_update_timestamp =  models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    
    objects = RatingManager()  #this gives access to two functions: Rating.objects.avg() and Rating.objects.all().avg
    
    class Meta:
        ordering = ["-timestamp"]
        
def rating_post_save(sender, instance, created, *args, **kwargs):
        if created:
            Suggestion=apps.get_model('suggestions', 'Suggestion')
            if instance.active:
                qs = Rating.objects.filter(
                    content_type= instance.content_type, user=instance.user, object_id=instance.object_id).exclude(
                        active=True, id=instance.id)
                if qs.exists():
                    qs = qs.exclude(active_update_timestamp__isnull=False)
                    qs.update(active=False, active_update_timestamp=datetime.now().astimezone(ISRAEL_TIMEZONE))
                suggestion_qs = Suggestion.objects.filter(
                    content_type= instance.content_type, user=instance.user, object_id=instance.object_id, did_rate=False)
                if suggestion_qs.exists():
                    suggestion_qs.update(did_rate=True, did_rate_timestamp=datetime.now().astimezone(ISRAEL_TIMEZONE), rating=instance.value)
                    
post_save.connect(rating_post_save, sender=Rating)