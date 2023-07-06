import os

from celery import Celery


# Set the default Django settings module for the 'celery' program.
'''to start on windows- two venv terminals in src: 
    celery -A home worker -l info -P gevent
    celery -A home beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
    start redis server 
    and python manage.py runserver
    to start jupiter :  python manage.py shell_plus --notebook   
    
'''


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'home.settings')

app = Celery('home')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
    
app.conf.beat_schedule = {
    "run_movie_rating_avg_every_3_min": {
        "task" : 'task_update_movie_ratings',
        "schedule":60*30,
    }, 
    # "generate_fake_reviews_every_min":
    #     {   "task" : "generate_fake_reviews", 
    #         "schedule":60*30,
    #         "kwargs":{"count":10000, "users":1000}
    #     }
      "run_export_rating_dataset_evey_hour": {
        "task" : 'export_rating_dataset',
        "schedule":60*60,
    },
}