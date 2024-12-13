from django.shortcuts import render
from .models import Movie
from django.http import JsonResponse
from .utils import fetch_popular_movies
from .utils import fetch_movies_from_tmdb
from .utils import fetch_genres
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import UserList
from django.views.decorators.csrf import csrf_exempt


def home(request):
    try:
        #Películas populares
        popular_movies = fetch_movies_from_tmdb("movie/popular")["results"][:10]

        #Series populares
        popular_series = fetch_movies_from_tmdb("tv/popular")["results"][:10]

        #Películas de animación
        animation_movies = fetch_movies_from_tmdb(
            "discover/movie", {"with_genres": 16}
        )["results"][:10]

        #Series de animación
        animation_series = fetch_movies_from_tmdb("discover/tv", {"with_genres": 16})[
            "results"
        ][:10]
        
        romance_movies = fetch_movies_from_tmdb(
            "discover/movie", {"with_genres": 10749}
        )["results"][:10]
        romance_series = fetch_movies_from_tmdb("discover/tv", {"with_genres": 10749})[
            "results"
        ][:10]

        action_movies = fetch_movies_from_tmdb("discover/movie", {"with_genres": 28})[
            "results"
        ][:10]
        action_series = fetch_movies_from_tmdb("discover/tv", {"with_genres": 10759})[
            "results"
        ][:10]

        documentary_movies = fetch_movies_from_tmdb(
            "discover/movie", {"with_genres": 99}
        )["results"][:10]
        documentary_series = fetch_movies_from_tmdb("discover/tv", {"with_genres": 99})[
            "results"
        ][:10]

        return render(
            request,
            "streaming/home.html",
            {
                "popular_movies": popular_movies,
                "popular_series": popular_series,
                "animation_movies": animation_movies,
                "animation_series": animation_series,
                "romance_movies": romance_movies,
                "romance_series": romance_series,
                "action_movies": action_movies,
                "action_series": action_series,
                "documentary_movies": documentary_movies,
                "documentary_series": documentary_series,
                "current_page": "home",
            },
        )
    except Exception as e:
        return render(
            request, "streaming/error.html", {"error_message": str(e)}, status=500
        )

def popular_movies(request):
    try:
        data = fetch_popular_movies()
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def movie_details(request, movie_id):
    try:
        # Llamar al endpoint de TMDb para detalles de la película
        movie_data = fetch_movies_from_tmdb(f"movie/{movie_id}")
        return render(
            request,
            "streaming/movie_detail.html",
            {"movie": movie_data, "movie_id": movie_id},
        )
    except Exception as e:
        return render(
            request, "streaming/error.html", {"error_message": str(e)}, status=500
        )


def series_list(request):
    try:
        country = request.GET.get("country")  #filtro por país
        genre = request.GET.get("genre")  #filtro por género
        params = {}
        if country:
            params["with_origin_country"] = country
        if genre:
            params["with_genres"] = genre

        series_data = fetch_movies_from_tmdb("discover/tv", params)
        series = series_data.get("results", [])

        sorted_series = sorted(
            series, key=lambda x: x.get("vote_average", 0), reverse=True
        )
        top_series = sorted_series[:20]
        genres = fetch_genres()

        return render(
            request,
            "streaming/series_list.html",
            {
                "series": top_series,
                "country": country,
                "genres": genres,
                "genre": genre,
            },
        )
    except Exception as e:
        return render(
            request, "streaming/error.html", {"error_message": str(e)}, status=500
        )


def series_details(request, series_id):
    try:
        series_data = fetch_movies_from_tmdb(f"tv/{series_id}")
        return render(request, "streaming/series_detail.html", {"series": series_data, "series_id": series_id})
    except Exception as e:
        return render(
            request, "streaming/error.html", {"error_message": str(e)}, status=500
        )


def movies_list(request):
    try:
        country = request.GET.get("country")
        genre = request.GET.get("genre") 
        params = {}
        if country:
            params["with_origin_country"] = country
        if genre:
            params["with_genres"] = genre

        for i in range(1, 6):
            params["page"] = i
        movies_data = fetch_movies_from_tmdb("discover/movie", params)
        movies = movies_data.get("results", [])

        sorted_movies = sorted(
            movies, key=lambda x: x.get("vote_average", 0), reverse=True
        )
        top_movies = sorted_movies[:30]

        genres = fetch_genres()

        return render(
            request,
            "streaming/movie_list.html",
            {
                "movies": top_movies,
                "country": country,
                "genres": genres,
                "genre": genre,
            },
        )
    except Exception as e:
        return render(
            request, "streaming/error.html", {"error_message": str(e)}, status=500
        )


def my_list(request):
    if not request.user.is_authenticated:
        return render(request, "streaming/my_list.html")
    user_list, created = UserList.objects.get_or_create(user=request.user)
    return render(
        request, "streaming/my_list.html", {"movies": user_list.movies_id.all()}
    )

@csrf_exempt
@login_required
def add_to_list_m(request, movie_id):
    return add_to_list(request, movie_id=movie_id)

@csrf_exempt
@login_required
def add_to_list_s(request, series_id):
    return add_to_list(request, series_id=series_id)

@csrf_exempt
@login_required
def add_to_list(request, movie_id="", series_id=""):
    if request.method == "POST":
        try:
            user_list, _ = UserList.objects.get_or_create(user=request.user)
            
            if not series_id:
                movie = Movie.objects.filter(tmdb_id=movie_id).first()
            else:
                movie = Movie.objects.filter(tmdb_id=series_id).first()
            
            if not movie:
                print(f"La película o serie con ID {movie_id} {series_id} no está en la base de datos.")
                if not series_id:
                    movie_data = fetch_movies_from_tmdb(f"movie/{movie_id}")
                    movie = Movie.objects.create(
                        title=movie_data["title"],
                        description=movie_data["overview"],
                        release_date=movie_data["release_date"],
                        poster_url="https://image.tmdb.org/t/p/w500"
                        + movie_data["poster_path"],
                        backdrop_url="https://image.tmdb.org/t/p/w500"
                        + movie_data["backdrop_path"],
                        tmdb_id=movie_data["id"],
                        is_series=False,
                    )
                    user_list.movies_id.add(movie)
                    return JsonResponse({"message": "Película añadida a tu lista"}, status=200)
                    
                else:
                    movie_data = fetch_movies_from_tmdb(f"tv/{series_id}")
                    serie = Movie.objects.create(
                        title=movie_data["name"],
                        description=movie_data["overview"],
                        release_date=movie_data["first_air_date"],
                        poster_url="https://image.tmdb.org/t/p/w500"
                        + movie_data["poster_path"],
                        backdrop_url="https://image.tmdb.org/t/p/w500"
                        + movie_data["backdrop_path"],
                        tmdb_id=movie_data["id"],
                        is_series=True,
                    )
                    user_list.movies_id.add(serie)

                    return JsonResponse({"message": "Serie añadida a tu lista"}, status=200)
            else:
                user_list.movies_id.add(movie)
                return JsonResponse({"message": "Película o serie añadida a tu lista"}, status=200)
        except Exception as e:
            return JsonResponse(
                {"message": f"Error al añadir la película o serie: {str(e)}"}, status=500
            )
    return JsonResponse({"message": "Método no permitido"}, status=405)


@login_required
def remove_from_list(request, movie_id):
    if request.method == "POST":
        movie = get_object_or_404(Movie, tmdb_id=movie_id)
        user_list = get_object_or_404(UserList, user=request.user)
        user_list.movies_id.remove(movie)
        return JsonResponse({"message": "Elemento eliminado de tu lista."})
