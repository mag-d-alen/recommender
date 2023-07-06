from celery import shared_task
from django.apps import apps
from machine_learning.utils import load_model, train_model
from movies.models import Movie
from django.contrib.contenttypes.models import ContentType
from suggestions.models import Suggestion
from user_profiles.utils import get_recent_users

@shared_task(name='train_surprise_model')
def train_surprise_model_task():
    train_model()
 

@shared_task(name='batch_user_prediction')
def batch_users_prediction_task(user_ids = None, start_page=0, offset=50, max_pages = 1000):
    model = load_model()
    Suggestion = apps.get_model('suggestions', 'Suggestion')
    c_type = ContentType.objects.get(model='movie')
    if not user_ids:
        user_ids = get_recent_users()
    end_page = start_page+offset
    movie_ids = Movie.objects.all().popular(reverse=True).values_list('id', flat=True)[start_page:end_page]
    recently_suggested =  Suggestion.objects.get_recently_suggested(movie_ids=movie_ids, user_ids=user_ids)
    suggestions=[]
    for movie_id in movie_ids:
        users_done = recently_suggested.get(f'{movie_id}') or []        
        for u_id in user_ids:
            if u_id in users_done:
                print(f'Movie {movie_id} suggested for user {u_id}')
                continue
            prediction = model.predict(uid = u_id, iid = movie_id).est   
            print(u_id, movie_id, prediction) 
            data={'content_type':c_type, 'user_id':u_id, 'object_id':movie_id, 'value':prediction}
            suggestions.append(Suggestion(**data))
    Suggestion.objects.bulk_create(suggestions, ignore_conflicts=True)
    if end_page < max_pages:
        return batch_users_prediction_task(start_page=end_page-1)
    
@shared_task(name='batch_update_user_prediction')
def batch_single_user_prediction_task(user_id=1, start_page=0, offset=50, max_pages = 1000):
    return batch_users_prediction_task(user_ids=[user_id], start_page=0, offset=50, max_pages = 1000)
    