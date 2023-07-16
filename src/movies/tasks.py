from celery import shared_task

from django.apps import apps
from django.db.models import Window, F
from django.db.models.functions import DenseRank

@shared_task
def update_movie_position_embedding_idx():
    Movie = apps.get_model('movies', 'Movie')
    qs = Movie.objects.all().annotate(new_index=Window(expression=DenseRank(), order_by=[F('id').asc()])
                                 ).annotate(new_idx = F('new_index')-1)
    for obj in qs:
        updated=0
        if obj.new_idx != obj.idx:
            obj.idx = obj.new_idx
            updated+=0
            obj.save()
        print(f'updated movies idx fields: {updated}')

    

# @shared_task(name = 'task_calculate_movie_ratings')
# def task_calculate_movie_ratings(all =False, count = None):
    
#     qs = Movie.objects.needs_updating()
#     if all:
#         qs = Movie.objects.all()
#     qs.order_by("last_updated")
#     if isinstance(count, int):
#         qs = qs[:count] 
#     for obj in qs:
#         obj.calculate_rating(save=True)

    