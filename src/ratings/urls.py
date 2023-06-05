from django.urls import path

from ratings.views import rate_movie_view


urlpatterns = [
    path('movie/', rate_movie_view)
]
