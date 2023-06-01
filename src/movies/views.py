from typing import Any, List
from django.db.models.query import QuerySet
from django.shortcuts import render

# Create your views here.
from django.views import generic

from movies.models import Movie

SORTING_CHOICES = {
    "popular":"-rating_avg", 
    "unpopular":"rating_avg", 
    "recent":"-release_date", 
    "old":"release_date", 
    
}


class MovieListView(generic.ListView):
    paginate_by=100
    context_object_name = 'movies'
    
    def get_template_names(self) -> List[str]:
        if self.request.htmx:
            return ['movies/snippet/list.html']
        return ["movies/list_view.html"]
    
    def get_queryset(self) -> QuerySet[Any]:
        queryset = Movie.objects.all()
        sort = self.request.GET.get('sort') 
        print(queryset, sort)
        if sort is not None:
             return queryset.order_by(sort)
        return queryset.order_by("-rating_avg")

    
    def get_context_data(self):    
        context = super().get_context_data()
        request = self.request
        user = request.user
        context['sorting_choices'] = SORTING_CHOICES
        if user.is_authenticated:
            movies_ids = [movie.id for movie in context['object_list']]         
            qs = user.rating_set.filter(object_id__in=movies_ids, active = True, content_type_id = 7)
            context["my_ratings"] = {f"{r.object_id}": r.value for r in qs}
        return context
    
    
    
class MovieDetailView(generic.DetailView):
    template_name = "movies/detail.html"
    queryset=Movie.objects.all()
    context_object_name = 'movie'

    def get_context_data(self, *args, **kwargs):    
        context = super().get_context_data()
        
        request = self.request
        user = request.user
        if user.is_authenticated:
            movie = context['movie']
            movies_ids = [movie.id]         
            qs = user.rating_set.filter(object_id__in=movies_ids, active = True, content_type_id = 7)
            context["my_ratings"] = {f"{r.object_id}": r.value for r in qs}
        return context