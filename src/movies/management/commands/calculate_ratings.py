from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from home.utils import get_fake_profiles, load_movie_data
from movies.tasks import task_calculate_movie_ratings
from ratings.models import Rating
from ratings.tasks import generate_fake_reviews



User = get_user_model()

class Command(BaseCommand):   
    def add_arguments(self, parser):
        parser.add_argument("--all", action="store_true", default=True)
        parser.add_argument("count", nargs="?", default=10, type=int)

    def handle(self, *args, **options):
        count = options.get("count")
        all = options.get("all")
        all_ratings = task_calculate_movie_ratings(all = all, count=count)
        if all:
            print(f" total = {Rating.objects.count()}")
        
     
