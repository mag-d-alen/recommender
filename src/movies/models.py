import zoneinfo
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models.query import QuerySet
from ratings.models import Rating, rating_post_save
import datetime as dt
from django.db.models import Q
# Create your models here.


RATING_UPDATE_DAYS = 1
ISRAEL_TIMEZONE = zoneinfo.ZoneInfo('Asia/Jerusalem')


class MovieQuerySet (models.QuerySet):
    def needs_updating(self):
        now = dt.datetime.now().astimezone(ISRAEL_TIMEZONE)
        update_delta = now - dt.timedelta(days = RATING_UPDATE_DAYS)
        qs = Movie.objects.filter(Q(last_updated__isnull=True)|
                                  Q(last_updated__lte=update_delta))
        
class MovieManager(models.Manager):
        def needs_updating(self):
            return self.get_queryset().needs_updating()
        def get_queryset(self) -> QuerySet:
            return MovieQuerySet(self.model, using=self._db)

 

class Movie(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=120, unique=True)
    overview= models.TextField()
    release_date = models.DateTimeField(blank=True, null=True, auto_now=False, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    ratings = GenericRelation(Rating) #queryset 
    rating_avg = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True)
    rating_count = models.IntegerField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null = True)

    objects = MovieManager()
        
    def calculate_ratings_count(self):
        return self.ratings.all().count()
    
    def calculate_ratings_avg(self):
        return self.ratings.all().avg()
    
    def calculate_rating(self, save=True):
        self.rating_avg = self.calculate_ratings_avg()
        self.rating_count = self.calculate_ratings_count()
        self.last_updated = dt.datetime.now().astimezone(ISRAEL_TIMEZONE)
        if save:
            self.save()
        return self.rating_avg
    
    def display_rating_avg(self):
        now = dt.datetime.now().astimezone(ISRAEL_TIMEZONE)
        if not self.last_updated:
            return self.calculate_rating()
        if self.last_updated > now - dt.timedelta(minutes=RATING_UPDATE_DAYS).astimezone(ISRAEL_TIMEZONE):
            return self.calculate_ratings_avg()
        return self.calculate_rating() 
    
    
    def get_absolute_url(self):
        return f"{self.id}"
    
    def __str__(self):
        if not self.release_date:
            return self.title
        return f"{self.title}, {self.release_date}"
           
    
    def __str__(self):
        return f"{self.id}__{self.title}"