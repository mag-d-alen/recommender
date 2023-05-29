from django.shortcuts import render

# Create your views here.
from django.views import generic

from movies.models import Movie

class MovieListView(generic.ListView):
    queryset = Movie.objects.all().order_by("-rating_avg")
    paginate_by=100
    template_name ="movies/list.html"
    context_object_name = 'movies'
    
    
    
class MovieDetailView(generic.DetailView):
    template_name = "movies/detail.html"
    queryset=Movie.objects.all()
    context_object_name = 'movie'
