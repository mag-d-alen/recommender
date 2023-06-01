
import random
from django.contrib.auth import get_user_model
from movies.models import Movie
from .models import Rating, RatingChoice
from celery import shared_task
from django.db.models import Avg, Count
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
User = get_user_model()

@shared_task(name = 'generate_fake_reviews' )
def generate_fake_reviews(count=100, users=10, null_avg=False):
    user_s =User.objects.first()
    user_e = User.objects.last()
    random_user_ids = random.sample(range(user_s.id, user_e.id),users)
    users = User.objects.filter(id__in=random_user_ids)
    movies = Movie.objects.all().order_by("?")[:count]
    if null_avg:
            movies = Movie.objects.filter(rating_avg__isnull = True).order_by("?")[:count]
    n_rating = movies.count() #should be == count
    rating_choices = [ x for x in RatingChoice.values if x is not None ]
    user_ratings = [random.choice(rating_choices) for _ in range(0, n_rating)]
    new_ratings = []
    for movie in movies: 
        #avoid bulk_create to be able to delete rating if user duplicates a rating with firing signal ( bulk create doesnt run post_save)
        rating_obj = Rating.objects.create(content_object = movie, value = user_ratings.pop(), user =random.choice(users))
        new_ratings.append(rating_obj.id)
    return new_ratings

@shared_task(name = 'task_update_movie_ratings')
def task_update_movie_ratings(object_id = None):
    ct = ContentType.objects.get_for_model(model=Movie) # this retrieves GeneralTypeKey relation
    rating_qs = Rating.objects.filter(content_type = ct)
    if object_id is not None:
        rating_qs = rating_qs.filter(object_id = object_id)
    agg_ratings = rating_qs.filter(content_type = ct).values('object_id')\
        .annotate(average = Avg('value'), count = Count('object_id'))
        # object_id is a part of ContentType model (CT stores values by object_id and pk)
    
    for rating in agg_ratings:
        qs = Movie.objects.filter(id= rating['object_id'])
        qs.update(rating_avg= rating['average'], rating_count=rating['count'], last_updated = timezone.now() )
        