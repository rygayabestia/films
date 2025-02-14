from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib import admin
urlpatterns = [
    path('admin/', admin.site.urls),
    path('movies/', include('movies.urls')),
    path('users/', include('users.urls')),
    # Перенаправляем корневой URL на список фильмов
    path('', RedirectView.as_view(url='/movies/')),
]