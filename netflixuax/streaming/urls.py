from django.urls import path
from .views import home
from .views import movie_details
from .views import series_list, series_details
from .views import movies_list
from .views import my_list, add_to_list, remove_from_list

app_name = "streaming"


urlpatterns = [
    path("", home, name="home"),
    path("series/", series_list, name="series-list"),
    path("series/<int:series_id>/", series_details, name="series-details-page"),
    path("movies/", movies_list, name="movies-list"),
    path("movie/<int:movie_id>/", movie_details, name="movie-details-page"),
    path("my-list/", my_list, name="my-list"),
    path("my-list/add/<int:movie_id>/", add_to_list, name="add-to-list"),
    path("my-list/remove/<int:movie_id>/", remove_from_list, name="remove-from-list"),
]
