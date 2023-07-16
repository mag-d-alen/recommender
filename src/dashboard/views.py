import re
from django.shortcuts import render
from movies.models import Movie
from suggestions.models import Suggestion

# Create your views here.
def dashboard_view(request):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return render(request, 'homepage.html',context )
    context['endless_path'] = '/'
    context['user'] = user
    suggestion_qs = Suggestion.objects.filter(user = user, did_rate=False)
    if suggestion_qs.exists():
        movie_ids = suggestion_qs.order_by('-value').values_list('object_id', flat=True)
        max_movie_count = 10
        request.session['total-new-suggestions'] = suggestion_qs.count()
        qs = Movie.objects.order_by_id(movie_ids)
        context['movies'] = qs[:max_movie_count]
    else:
        context['movies'] = Movie.objects.all().order_by('?')
    if request.htmx:
        return render(request, 'movies/snippet/infinite.html', context)
    return render(request, 'dashboard/main.html', context) 