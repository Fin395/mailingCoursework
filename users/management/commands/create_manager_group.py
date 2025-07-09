from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    help = 'Создание группы Менеджеры'

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name='Менеджеры')
        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Менеджеры" создана.'))
        else:
            self.stdout.write(self.style.WARNING('Группа "Менеджеры" уже существует.'))
