import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from .models import Movie
from users.models import User, Liked
from django.core.paginator import Paginator

def fetch_movie_data(movie_id):
    url = f'https://api.kinopoisk.dev/v1.3/movie/{movie_id}'
    headers = {'X-API-KEY': settings.KINOPOISK_API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def movie_list(request):
    all_movies = Movie.objects.all()
    genres = set()
    for movie in all_movies:
        movie_data = fetch_movie_data(movie.movie_id)
        if movie_data and 'genres' in movie_data:
            for genre in movie_data['genres']:
                genres.add(genre['name'])

    selected_genres = request.GET.getlist('genres')
    movies = []
    if selected_genres:
        for movie in all_movies:
            movie_data = fetch_movie_data(movie.movie_id)
            if movie_data and 'genres' in movie_data:
                movie_genres = [genre['name'] for genre in movie_data['genres']]
                if any(genre in movie_genres for genre in selected_genres):
                    movies.append(movie_data)

    liked_movie_ids = []
    if request.session.get('user_id'):
        user_id = request.session['user_id']
        liked_movie_ids = Liked.objects.filter(user_id=user_id).values_list('movie_id', flat=True)

    paginator = Paginator(movies, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'movies/movie_list.html', {
        'movies': movies,
        'genres': sorted(genres),
        'selected_genres': selected_genres,
        'liked_movie_ids': liked_movie_ids,
    })

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, movie_id=movie_id)
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

def like_movie(request, movie_id):
    if not request.session.get('user_id'):
        return redirect('login')

    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    movie = get_object_or_404(Movie, id=movie_id)

    if not Liked.objects.filter(user=user, movie=movie).exists():
        Liked.objects.create(user=user, movie=movie)

    return redirect('movie_detail', movie_id=movie_id)