from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.http import require_http_methods
from ratings.models import Rating

@require_http_methods('POST')
def rate_movie_view(request):
    if not request.htmx:
        return HttpResponse('Not Allowed', status= 400)
    movie_id = request.POST.get('movie_id')
    rating = request.POST.get('rating_value')
    if movie_id is None or rating is None:
        response = HttpResponse('skipping')
        response['HX-Trigger']='skipped'
        return response
    user  =  request.user
    message ='<span>Please <a href="/accounts/login">login</a> to rate the movie</span>'
    if user.is_authenticated:
        message ='<span class = "bg-danger text-light px-3 py-1 rounded">An errror occured</span>'
        ctype = ContentType.objects.get(app_label = 'movies', model = 'movie' )
        rating_obj = Rating.objects.create(content_type=ctype, object_id=movie_id, user=user, value=rating)
        if rating_obj.content_object is not None:
            message ='<span class = "bg-success text-light p-1 smaller rounded">Rating successful!</span>'
            response = HttpResponse(message, status= 200)
            response['HX-Trigger-After-Settle']='rated'
            return response
    return HttpResponse(message, status = 200)
        
        
        