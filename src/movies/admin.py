from django.contrib import admin
from movies.models import Movie
# Register your models here.

class MovieAdmin(admin.ModelAdmin):
    model = Movie
    list_display = ["__str__", "calculate_ratings_count", "rating_avg", "last_updated"]
    readonly_fields = ["rating_avg","rating_count","display_rating_avg"]
    search_fields = ["title"]
    
    
admin.site.register(Movie, MovieAdmin)
