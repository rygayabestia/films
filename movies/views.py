<<<<<<< HEAD
import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from .models import Movie
from users.models import User, Liked
from django.core.paginator import Paginator

def fetch_movie_data(movie_id):
    url = f'https://api.kinopoisk.dev/v1.3/movie/{movie_id}'
    headers = {'X-API-KEY': settings.KINOPOISK_API_KEY}
=======
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
>>>>>>> 7a7e6d19eb1e3ac72be796a606af44a0a13132b2
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def movie_list(request):
    all_movies = Movie.objects.all().order_by('title')  # Сортируем по названию
    genres = set()
<<<<<<< HEAD
    for movie in all_movies:
        movie_data = fetch_movie_data(movie.movie_id)
        if movie_data and 'genres' in movie_data:
            for genre in movie_data['genres']:
                genres.add(genre['name'])
=======
>>>>>>> 7a7e6d19eb1e3ac72be796a606af44a0a13132b2

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
<<<<<<< HEAD
            movie_data = fetch_movie_data(movie.movie_id)
            if movie_data and 'genres' in movie_data:
                movie_genres = [genre['name'] for genre in movie_data['genres']]
                if any(genre in movie_genres for genre in selected_genres):
                    movies.append(movie_data)
=======
            api_data = get_movie_info_from_api(movie.movie_id)
            if api_data and any(genre['genre'] in selected_genres for genre in api_data.get('genres', [])):
                movies.append(movie)
    else:
        movies = list(all_movies)  # Преобразуем QuerySet в список
>>>>>>> 7a7e6d19eb1e3ac72be796a606af44a0a13132b2

    liked_movie_ids = []
    if request.session.get('user_id'):
        user_id = request.session['user_id']
        liked_movie_ids = Liked.objects.filter(user_id=user_id).values_list('movie_id', flat=True)

    # Пагинация
    paginator = Paginator(movies, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'movies/movie_list.html', {
<<<<<<< HEAD
        'movies': movies,
=======
        'movies': page_obj,
>>>>>>> 7a7e6d19eb1e3ac72be796a606af44a0a13132b2
        'genres': sorted(genres),
        'selected_genres': selected_genres,
        'liked_movie_ids': liked_movie_ids,
    })


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, movie_id=movie_id)
<<<<<<< HEAD
    movie_data = fetch_movie_data(movie.movie_id)
    if not movie_data:
        return render(request, 'movies/movie_detail.html', {
            'error': 'Фильм не найден',
        })

    return render(request, 'movies/movie_detail.html', {
        'movie': movie_data,
        'poster_url': movie_data.get('poster', {}).get('url', ''),
        'description': movie_data.get('description', ''),
        'rating': movie_data.get('rating', {}).get('kp', 0),
        'genres': [genre['name'] for genre in movie_data.get('genres', [])],
    })
=======
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
>>>>>>> 7a7e6d19eb1e3ac72be796a606af44a0a13132b2

def like_movie(request, movie_id):
    if not request.session.get('user_id'):
        return redirect('login')

    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
<<<<<<< HEAD
    movie = get_object_or_404(Movie, id=movie_id)
=======
    movie = get_object_or_404(Movie, movie_id=movie_id)
>>>>>>> 7a7e6d19eb1e3ac72be796a606af44a0a13132b2

    if not Liked.objects.filter(user=user, movie=movie).exists():
        Liked.objects.create(user=user, movie=movie)

    return redirect('movie_detail', movie_id=movie_id)