from movies.models import Movie
from celery import shared_task


@shared_task(name = 'task_calculate_movie_ratings')
def task_calculate_movie_ratings(all =False, count = None):
    
    qs = Movie.objects.needs_updating()
    if all:
        qs = Movie.objects.all()
    qs.order_by("last_updated")
    if isinstance(count, int):
        qs = qs[:count] 
    for obj in qs:
        obj.calculate_rating(save=True)

    