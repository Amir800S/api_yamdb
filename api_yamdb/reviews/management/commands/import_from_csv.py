import csv

from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

import api_yamdb.settings
from reviews.models import (Category, Comment, Genre,
                            Review, Title, User, GenreTitle)

CSV_FILES = {Category: 'category.csv',
             Genre: 'genre.csv',
             Title: 'titles.csv',
             GenreTitle: 'genre_title.csv',
             User: 'users.csv',
             Review: 'review.csv',
             Comment: 'comments.csv'}

REPLACE_FIELDS = {Title: ['category', 'category_id'],
                  Review: ['author', 'author_id'],
                  Comment: ['author', 'author_id']}


def del_data():
    """Удаляет все таблицы из базы данных"""
    for model in CSV_FILES:
        model.objects.all().delete()


class Command(BaseCommand):
    """Команда очищает БД"""
    def add_arguments(self, parser):
        parser.add_argument(
            '-d',
            '--delete',
            action='store_true',
            help='Удаляет все данные из базы данных'
        )

    def handle(self, *args, **options):
        '''Импорт в БД'''
        if options['delete']:
            del_data()
            self.stdout.write('База данных успешно очищена.')
        else:
            for model, csv_file in CSV_FILES.items():
                file = f'{api_yamdb.settings.BASE_DIR}/static/data/{csv_file}'
                with open(f'{file}',
                          'r', encoding='utf8') as file:
                    for row in csv.DictReader(file, delimiter=','):
                        if model in REPLACE_FIELDS:
                            row[REPLACE_FIELDS[model][1]] = row.pop(
                                REPLACE_FIELDS[model][0])
                        try:
                            model.objects.create(**row)
                        except ValueError as e:
                            raise CommandError(
                                f'Ошибка: {e}, файл {file}, строка {row}'
                            )
                        except IntegrityError as error:
                            raise CommandError(f'База данных уже заполнена.'
                                               f'Необходимо очистить БД.'
                                               f'Ошибка {error}.'
                                               f'Для очистки БД'
                                               f'используйте --delete.')
                self.stdout.write(f'Таблица {model.__name__} импортирована!')
