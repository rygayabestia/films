import csv
import django
import pandas
from django.core.management.base import BaseCommand
from movies.models import Movie

class Command(BaseCommand):
    help = 'Load movies from CSV'

    def handle(self, *args, **kwargs):
        with open('movie_data.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                genres = {key: value for key, value in row.items() if key not in ['Фильмы', 'movie_id']}
                Movie.objects.create(
                    title=row['Фильмы'],
                    genres=genres,
                    movie_id=row['movie_id']
                )
        self.stdout.write(self.style.SUCCESS('Successfully loaded movies'))