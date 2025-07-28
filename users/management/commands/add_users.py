from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from users.models import User


class Command(BaseCommand):
    help = "Создание тестовых пользователей"

    def handle(self, *args, **kwargs):
        # Удаляем существующих пользователей
        User.objects.all().delete()

        # Создаем или обновляем группу managers
        managers_group, created = Group.objects.get_or_create(name='managers')
        if created:
            self.stdout.write(self.style.SUCCESS('Группа managers создана'))

        # Добавляем разрешение
        try:
            permission = Permission.objects.get(codename='can_disable_user')
            managers_group.permissions.add(permission)
            self.stdout.write(self.style.SUCCESS('Разрешение добавлено в группу managers'))
        except Permission.DoesNotExist:
            self.stdout.write(self.style.ERROR('Разрешение "can_disable_user" не найдено'))

        # Список пользователей для создания
        users_data = [
            # Обычные пользователи
            {
                "email": "test1@example.com",
                "first_name": "Алла",
                "last_name": "Быкова",
                "is_manager": False
            },

            # Менеджеры
            {
                "email": "test2@example.com",
                "first_name": "Сергей",
                "last_name": "Васнецов",
                "is_manager": True
            },
            {
                "email": "test3@example.com",
                "first_name": "Андрей",
                "last_name": "Кочкин",
                "is_manager": True
            },
        ]

        # Создаем пользователей
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                email=user_data["email"],
                defaults={
                    "first_name": user_data["first_name"],
                    "last_name": user_data["last_name"],
                    "is_superuser": user_data.get("is_superuser", False),
                    "is_staff": user_data.get("is_staff", False),
                    "is_active": True
                }
            )

            # Устанавливаем пароль
            if created:
                user.set_password("testpassword123")
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Создан пользователь: {user.email}'))

            # Добавляем в группу managers
            if user_data.get("is_manager", False):
                user.groups.add(managers_group)
                self.stdout.write(self.style.SUCCESS(f'Пользователь {user.email} добавлен в группу managers'))

        self.stdout.write(self.style.SUCCESS('Все пользователи успешно созданы'))
