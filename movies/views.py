from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie
from django.core.paginator import Paginator
from users.models import Liked, User
import requests
from django.conf import settings

def get_movie_info_from_api(movie_id):
    url = f"https://api.kinopoisk.dev/v1.3/movie/{movie_id}"
    headers = {
        "X-API-KEY": settings.KINOPOISK_API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def movie_list(request):
    all_movies = Movie.objects.all().order_by('title')  # Сортируем по названию
    genres = set()

    # Получаем уникальные жанры из API
    for movie in all_movies:
        api_data = get_movie_info_from_api(movie.movie_id)
        if api_data:
            for genre in api_data.get('genres', []):
                genres.add(genre['genre'])

    # Фильтрация по выбранным жанрам
    selected_genres = request.GET.getlist('genres')
    movies = []
    if selected_genres:
        for movie in all_movies:
            api_data = get_movie_info_from_api(movie.movie_id)
            if api_data and any(genre['genre'] in selected_genres for genre in api_data.get('genres', [])):
                movies.append(movie)
    else:
        movies = list(all_movies)  # Преобразуем QuerySet в список

    # Получаем список лайкнутых фильмов для текущего пользователя
    liked_movie_ids = []
    if request.session.get('user_id'):
        user_id = request.session['user_id']
        liked_movie_ids = Liked.objects.filter(user_id=user_id).values_list('movie_id', flat=True)

    # Пагинация
    paginator = Paginator(movies, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'movies/movie_list.html', {
        'movies': page_obj,
        'genres': sorted(genres),
        'selected_genres': selected_genres,
        'liked_movie_ids': liked_movie_ids,
    })


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, movie_id=movie_id)
    api_data = get_movie_info_from_api(movie.movie_id)

    if api_data:
        filtered_genres = {genre['genre']: 'A' for genre in api_data.get('genres', [])}
        context = {
            'movie': movie,
            'filtered_genres': filtered_genres,
            'api_data': api_data,
        }
    else:
        filtered_genres = {genre: value for genre, value in movie.genres.items() if value == 'A'}
        context = {
            'movie': movie,
            'filtered_genres': filtered_genres,
        }

    return render(request, 'movies/movie_detail.html', context)

def like_movie(request, movie_id):
    if not request.session.get('user_id'):
        return redirect('login')

    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    movie = get_object_or_404(Movie, movie_id=movie_id)

    if not Liked.objects.filter(user=user, movie=movie).exists():
        Liked.objects.create(user=user, movie=movie)

    return redirect('movie_detail', movie_id=movie_id)