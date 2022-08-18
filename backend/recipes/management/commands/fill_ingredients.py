from csv import reader

from django.core.management import BaseCommand, CommandError

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Fill ingredients to database'

    def handle(self, *args, **kwargs):
        try:
            with open('data/ingredients.csv', 'r',
                      encoding='UTF-8') as ingredients:
                for row in reader(ingredients):
                    Ingredient.objects.get_or_create(
                        name=row[0], measurement_unit=row[1],
                    )
        except Exception:
            raise CommandError('Что-то пошло не так')
        self.stdout.write(
            self.style.SUCCESS('Успешно!'))
