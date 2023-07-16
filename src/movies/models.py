import zoneinfo
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models.query import QuerySet
from django.forms import FloatField
import datetime as dt
from django.db.models import Q, F, Sum, Case, When
from django.db.models.signals import post_delete, post_save
from movies.tasks import update_movie_position_embedding_idx 

from ratings.models import Rating
# Create your models here.


RATING_UPDATE_DAYS = 1
ISRAEL_TIMEZONE = zoneinfo.ZoneInfo('Asia/Jerusalem')


class MovieQuerySet (models.QuerySet):
    
    def popular(self, reverse=False): 
        ordering = '-score'
        if reverse:
            ordering = 'score'
        return self.annotate(score=Sum(F('rating_avg')*F('rating_count'), output_fields = models.FloatField)).order_by(ordering)
        
    def needs_updating(self):
        now = dt.datetime.now().astimezone(ISRAEL_TIMEZONE)
        update_delta = now - dt.timedelta(days = RATING_UPDATE_DAYS)
        return self.filter(Q(last_updated__isnull=True)|
                                  Q(last_updated__lte=update_delta))
 
        
class MovieManager(models.Manager):
        def needs_updating(self):
            return self.get_queryset().needs_updating()
        def get_queryset(self) -> QuerySet:
            return MovieQuerySet(self.model, using=self._db)
        def order_by_id(self, movie_pks=[]):
            qs = self.get_queryset().filter(pk__in=movie_pks)
            id_ordering = Case(*[When(pk=pk, then=idx) for idx, pk in enumerate(movie_pks)])
            return qs.order_by(id_ordering)
                

 

class Movie(models.Model):
    id = models.BigAutoField(primary_key=True)
    idx = models.IntegerField(blank=True, null=True, help_text='continuous position for ml')
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


def movie_post_save(instance, created, *args, **kwargs):
    if created and instance.id:    
        update_movie_position_embedding_idx()
post_save.connect(movie_post_save, sender=Movie)


def movie_post_delete(*args, **kwargs):
    update_movie_position_embedding_idx()       
post_delete.connect(movie_post_delete, sender=Movie)