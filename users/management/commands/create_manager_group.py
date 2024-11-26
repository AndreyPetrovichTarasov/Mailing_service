from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Создает группу "Менеджеры" в базе данных'

    def handle(self, *args, **kwargs):
        group_name = "Managers"

        if Group.objects.filter(name=group_name).exists():
            self.stdout.write(self.style.WARNING(f'Группа "{group_name}" уже существует.'))
        else:
            Group.objects.create(name=group_name)
            self.stdout.write(self.style.SUCCESS(f'Группа "{group_name}" успешно создана.'))
