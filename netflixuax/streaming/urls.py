from django.urls import path
from .views import MovieListView, MovieDetailView, PlaylistView, RecommendationView, home, base
from .views import popular_movies, movie_details
from .views import series_list, series_details
from .views import movies_list

app_name = 'streaming'


urlpatterns = [
    path('', home, name='home'),
    path('base/', base, name='base'),
    path('series/', series_list, name='series-list'),
    path('series/<int:series_id>/', series_details, name='series-details-page'),
    path('movies/', movies_list, name='movies-list'),
    path('movie/<int:movie_id>/', movie_details, name='movie-details-page'),
    
    path('api/popular/', popular_movies, name='popular-movies'),
    path('api/movie/<int:movie_id>/', movie_details, name='movie-details'),
    path('api/movies/', MovieListView.as_view(), name='movie-list'),
    path('api/movies/<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),
    path('api/playlists/', PlaylistView.as_view(), name='playlist'),
    path('api/recommendations/', RecommendationView.as_view(), name='recommendation'),
]
    
