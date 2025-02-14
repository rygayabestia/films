from django.shortcuts import render, get_object_or_404
from .models import Movie
from django.shortcuts import redirect
from users.models import User
from django.core.paginator import Paginator


def movie_list(request):
    # Получаем все уникальные жанры из базы данных
    all_movies = Movie.objects.all()
    genres = set()
    for movie in all_movies:
        for genre, value in movie.genres.items():
            if value == 'A':  # Если жанр присутствует в фильме
                genres.add(genre)

    # Получаем выбранные жанры из GET-запроса
    selected_genres = request.GET.getlist('genres')

    # Фильтруем фильмы по выбранным жанрам
    movies = []
    if selected_genres:  # Если выбраны жанры
        for movie in all_movies:
            # Проверяем, есть ли у фильма все выбранные жанры
            if all(movie.genres.get(genre) == 'A' for genre in selected_genres):
                movies.append(movie)

    # Пагинация: разбиваем фильмы на страницы
    paginator = Paginator(movies, 10)  # Показываем 10 фильмов на странице
    page_number = request.GET.get('page')  # Получаем номер страницы из GET-запроса
    page_obj = paginator.get_page(page_number)  # Получаем объект страницы

    # Передаем данные в шаблон
    return render(request, 'movies/movie_list.html', {
        'page_obj': page_obj,  # Передаем объект страницы
        'genres': sorted(genres),  # Сортируем жанры для удобства
        'selected_genres': selected_genres,
        'show_movies': bool(selected_genres),  # Флаг для отображения фильмов
    })


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, movie_id=movie_id)

    # Фильтруем жанры, оставляем только те, которые отмечены 'A'
    filtered_genres = {genre: value for genre, value in movie.genres.items() if value == 'A'}

    return render(request, 'movies/movie_detail.html', {
        'movie': movie,
        'filtered_genres': filtered_genres,
    })


def like_movie(request, movie_id):
    if not request.user.is_authenticated:
        return redirect('login')
    movie = get_object_or_404(Movie, movie_id=movie_id)
    user = User.objects.get(id=request.user.id)
    if movie in user.liked_movies.all():
        user.liked_movies.remove(movie)
    else:
        user.liked_movies.add(movie)
    return redirect('movie_detail', movie_id=movie_id)