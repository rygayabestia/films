from django.urls import path
from . import views
from movies.views import movie_detail  # Импортируем представление из приложения movies

urlpatterns = [
    path('like/<int:movie_id>/', views.like_movie, name='like_movie'),
    path('movie/<int:movie_id>/', movie_detail, name='movie_detail'),  # Используем импортированное представление
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]