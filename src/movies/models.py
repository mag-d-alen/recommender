from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from ratings.models import Rating

# Create your models here.
class Movie(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=120, unique=True)
    overview= models.TextField()
    release_date = models.DateTimeField(blank=True, null=True, auto_now=False, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    ratings = GenericRelation(Rating)
    
    def calculate_ratings_count(self):
        return self.ratings.all().count()
    
    def calculate_ratings_avg(self):
        return self.ratings.all().count()
    
    def __str__(self):
        return f"{self.id}__{self.title}"