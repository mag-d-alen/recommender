from django.contrib import admin
from movies.models import Movie
# Register your models here.


class MovieAdmin(admin.ModelAdmin):
    model = Movie
    list_display = ["__str__", "idx","rating_avg", "last_updated", "rating_count"]
    readonly_fields = ["rating_avg", "rating_count", "idx",]
    search_fields = ["title"]


admin.site.register(Movie, MovieAdmin)
