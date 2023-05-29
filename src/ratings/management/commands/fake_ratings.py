from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from home.utils import get_fake_profiles, load_movie_data
from movies.models import Movie
from ratings.models import Rating
from ratings.tasks import generate_fake_reviews



User = get_user_model()

class Command(BaseCommand):   
    def add_arguments(self, parser):
        parser.add_argument("count", nargs="?", default=10, type=int)
        parser.add_argument("--users", default = 1000, type=int)
        parser.add_argument("--show-total", action="store_true", default=True)



    
    def handle(self, *args, **options):
        count = options.get("count")
        show_total = options.get("show_total")
        users_count = options.get("users")
        generated_ratings=generate_fake_reviews(count=count, users=users_count)
        if show_total:
            print(f"{len(generated_ratings)}, total = {Rating.objects.count()}")
        
     
