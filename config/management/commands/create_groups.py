from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from mailings.models import Mailing


class Command(BaseCommand):
    help = 'Назначает разрешения для группы "moderators"'

    def handle(self, *args, **kwargs):
        """
        Получаем группу "moderators" или создаем её, если не существует
        """
        moderators, created = Group.objects.get_or_create(name='moderators')

        """
        Получаем разрешения для модели Mailing
        """
        content_type = ContentType.objects.get_for_model(Mailing)

        """
        Стандартные разрешения для модели Mailing
        """
        permissions = Permission.objects.filter(content_type=content_type)

        """
        Добавляем разрешения для группы
        """
        for permission in permissions:
            moderators.permissions.add(permission)

        """
        Добавляем кастомные разрешения
        Пример добавления кастомного разрешения, если оно есть
        Например, разрешение на снятие товара с публикации
        """
        custom_permission = Permission.objects.get(codename='can_unpublish_product')
        moderators.permissions.add(custom_permission)

        self.stdout.write(self.style.SUCCESS('Права успешно назначены группе "moderators"'))
