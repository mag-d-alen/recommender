from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from home.utils import get_fake_profiles, load_movie_data
from movies.models import Movie



User = get_user_model()

class Command(BaseCommand):
    
    def add_arguments(self, parser):
        parser.add_argument("count", nargs="?", default=10, type=int)
        parser.add_argument("--users", action="store_true", default=False)
        parser.add_argument("--movies", action="store_true", default=False)
        parser.add_argument("--show-total", action="store_true", default=False)


    
    def handle(self, *args, **options):
        count = options.get("count")
        show_total = options.get("show_total")
        load_movies = options.get("movies")
        generate_users = options.get("users")
        if load_movies:
            movie_dataset = load_movie_data(limit = count)
            movies= [Movie(**item) for item in movie_dataset]
            added_movies = Movie.objects.bulk_create(movies, ignore_conflicts=True)
            print(f"Movies created: len(added_movies)")
            if show_total:
                print(f"Total movies created: {Movie.objects.count()}")
        if generate_users:
            profiles = get_fake_profiles(count = count)
            all_users = [User(**profile) for profile in profiles]
            users_bulk = User.objects.bulk_create(all_users, ignore_conflicts=True)
            print(f"new users : {len(users_bulk)}")
            if show_total:
                print(f"Total users:{User.objects.count()}")
                
