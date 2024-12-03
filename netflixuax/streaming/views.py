from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Movie, Playlist, Recommendation
from .serializers import MovieSerializer, PlaylistSerializer, RecommendationSerializer
from django.http import JsonResponse, HttpResponse
from .utils import fetch_popular_movies, fetch_movie_details
from .scripts.import_movies import fetch_and_store_movies
from .utils import fetch_movies_from_tmdb
from .utils import fetch_genres
# Vista Home para plantillas
def home(request):
    print("Requesting home")
    # fetch_and_store_movies()
    movies = Movie.objects.all()
    return render(request, 'streaming/home.html', {'movies': movies})

# Vista Home para plantillas
def base(request):
    print("Requesting home")
    # fetch_and_store_movies()
    # movies = Movie.objects.all()
    return render(request, 'streaming/base.html')

# Vistas para la API
class MovieListView(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

class MovieDetailView(APIView):
    def get(self, request, pk):
        try:
            movie = Movie.objects.get(pk=pk)
            serializer = MovieSerializer(movie)
            return Response(serializer.data)
        except Movie.DoesNotExist:
            return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)

class PlaylistView(APIView):
    def get(self, request):
        playlists = Playlist.objects.filter(user=request.user)
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        playlist = Playlist.objects.create(name=data['name'], user=request.user)
        if 'movies' in data:
            for movie_id in data['movies']:
                movie = Movie.objects.get(id=movie_id)
                playlist.movies.add(movie)
        playlist.save()
        return Response(PlaylistSerializer(playlist).data, status=status.HTTP_201_CREATED)

class RecommendationView(APIView):
    def get(self, request):
        try:
            recommendation = Recommendation.objects.get(user=request.user)
            serializer = RecommendationSerializer(recommendation)
            return Response(serializer.data)
        except Recommendation.DoesNotExist:
            return Response({"message": "No recommendations found."}, status=status.HTTP_404_NOT_FOUND)



def popular_movies(request):
    """Vista para obtener películas populares."""
    try:
        data = fetch_popular_movies()
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# carpeta: streaming/views.py
def movie_details(request, movie_id):
    """Vista para mostrar detalles de una película específica."""
    try:
        # Llamar al endpoint de TMDb para detalles de la película
        movie_data = fetch_movies_from_tmdb(f'movie/{movie_id}')
        return render(request, 'streaming/movie_detail.html', {'movie': movie_data})
    except Exception as e:
        return render(request, 'streaming/error.html', {'error_message': str(e)}, status=500)

# carpeta: streaming/views.py
# carpeta: streaming/views.py
# carpeta: streaming/views.py
def series_list(request):
    """Vista para mostrar series populares, con filtros por país y género."""
    try:
        country = request.GET.get('country')  # Obtener filtro por país
        genre = request.GET.get('genre')  # Obtener filtro por género
        params = {}
        if country:
            params['with_origin_country'] = country
        if genre:
            params['with_genres'] = genre
        
        # Llamar a TMDb con filtros aplicados
        series_data = fetch_movies_from_tmdb('discover/tv', params)
        series = series_data.get('results', [])

        # Ordenar por rating y limitar
        sorted_series = sorted(series, key=lambda x: x.get('vote_average', 0), reverse=True)
        top_series = sorted_series[:20]
        
        # Obtener géneros disponibles
        genres = fetch_genres()

        return render(request, 'streaming/series_list.html', {
            'series': top_series,
            'country': country,
            'genres': genres,
            'genre': genre
        })
    except Exception as e:
        return render(request, 'streaming/error.html', {'error_message': str(e)}, status=500)
    

# carpeta: streaming/views.py
def series_details(request, series_id):
    """Vista para mostrar detalles de una serie específica."""
    try:
        # Llamar al endpoint de TMDb para detalles de la serie
        series_data = fetch_movies_from_tmdb(f'tv/{series_id}')
        return render(request, 'series_detail.html', {'series': series_data})
    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)}, status=500)
    
    
    
# carpeta: streaming/views.py
def movies_list(request):
    """Vista para mostrar películas populares, con filtros por país y género."""
    try:
        country = request.GET.get('country')  # Filtro por país
        genre = request.GET.get('genre')  # Filtro por género
        params = {}
        if country:
            params['with_origin_country'] = country
        if genre:
            params['with_genres'] = genre
        
        # Usar el endpoint de descubrimiento para películas
        for i in range(1, 6):
            params['page'] = i
        movies_data = fetch_movies_from_tmdb('discover/movie', params)
        movies = movies_data.get('results', [])
        
        # Ordenar por rating
        sorted_movies = sorted(movies, key=lambda x: x.get('vote_average', 0), reverse=True)
        top_movies = sorted_movies[:30]
        
        # Obtener lista de géneros disponibles
        genres = fetch_genres()

        return render(request, 'movie_list.html', {
            'movies': top_movies,
            'country': country,
            'genres': genres,
            'genre': genre
        })
    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)}, status=500)


