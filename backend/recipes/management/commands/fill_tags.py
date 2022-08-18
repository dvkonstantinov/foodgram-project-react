from csv import reader

from django.core.management.base import BaseCommand, CommandError

from recipes.models import Tag


class Command(BaseCommand):
    help = 'Fill tags to database'

    def handle(self, *args, **kwargs):
        try:
            with open('data/tags.csv', 'r',
                      encoding='UTF-8') as tags:
                for row in reader(tags):
                    Tag.objects.get_or_create(
                        name=row[0], color=row[1], slug=row[2],
                    )
        except Exception:
            raise CommandError('Что-то пошло не так')
        self.stdout.write(
            self.style.SUCCESS('Успешно!'))
