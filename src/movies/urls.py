from django.urls import path
from movies.views import MovieDetailView, MovieListView


urlpatterns = [  
    path('', MovieListView.as_view()),
    path('<int:pk>/', MovieDetailView.as_view()),
 ]