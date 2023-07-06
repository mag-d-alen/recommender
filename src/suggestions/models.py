from django.db import models

# Create your models here.
from datetime import datetime
import zoneinfo
from django.apps import apps
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType 
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.query import QuerySet
from django.db.models import Avg, F
from django.db.models.signals import post_save
from django.utils import timezone


# Create your models here.

User = settings.AUTH_USER_MODEL
ISRAEL_TIMEZONE = zoneinfo.ZoneInfo('Asia/Jerusalem')


    
class SuggestionQuerySet(models.QuerySet):
    def avg(self):
        return self.aggregate(average=Avg("value")) ["average"] #creates a dict {"avarage": value}
    
    def movies(self):
        ctype = ContentType.objects.get_for_model(apps.get_model('movies', 'Movie')) #to avoid circular import
        return self.filter(active=True, content_type=ctype)



class SuggestionManager(models.Manager):
    def get_recently_suggested(self, movie_ids=[], user_ids=[], days_ago=7):
        delta= datetime.timedelta(days=days_ago)
        time_delta = timezone.now()-delta
        data={}
        ctype=ContentType.objects.get(app_label='movies', model='movie')
        dataset=self.get_queryset().filter(content_type=ctype, object_id__in=movie_ids, user_id__in=user_ids,timestamp__gte=time_delta, active =True).values('object_id', 'user_id')
        for d in dataset:
            movie_id = str(d.get('object_id'))
            user_id = d.get('user_id')
            if movie_id in data:
                data[movie_id].append(user_id)
            else:
                data[movie_id]=[user_id]
        return data 
    
    
class Suggestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.FloatField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id= models.PositiveIntegerField() 
    content_object = GenericForeignKey("content_type", "object_id") 
    timestamp = models.DateTimeField(default=timezone.now)
    
    # when ratings occur after a suggestion
    rating = models.FloatField(blank=True, null=True)
    active = models.BooleanField(default=True)
    did_rate = models.BooleanField(default=False)
    did_rate_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
    
    objects = SuggestionManager()
    
    
    class Meta:
        ordering = ["-timestamp"]
