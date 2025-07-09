from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    help = 'Создание группы Менеджеры'

    def handle(self, *args, **kwargs):
        managers_group, created = Group.objects.get_or_create(name='Менеджеры')
        if created:
            add_perm = Permission.objects.get(codename='add_mailing')  # замените modelname на имя вашей модели
            change_perm = Permission.objects.get(codename='change_mailing')
            managers_group.permissions.add(add_perm, change_perm)
            self.stdout.write(self.style.SUCCESS('Группа "Менеджеры" создана.'))
        else:
            self.stdout.write(self.style.WARNING('Группа "Менеджеры" уже существует.'))
