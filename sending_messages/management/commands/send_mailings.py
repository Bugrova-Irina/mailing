from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from sending_messages.models import Mailing, AttemptToSend


class Command(BaseCommand):
    help = 'Отправка активных рассылок с отчетом по каждому получателю'

    def handle(self, *args, **options):
        current_time = timezone.now()
        self.stdout.write(f'== Запуск обработки рассылок в {current_time} ==')

        # Автоматическое обновление статусов рассылок
        updated_completed = Mailing.objects.filter(
            status=Mailing.STARTED,
            end_sending__lt=current_time
        ).update(status=Mailing.COMPLETED)

        self.stdout.write(f'Обновлено статусов завершенных рассылок: {updated_completed}')

        # Поиск активных рассылок для обработки
        active_mailings = Mailing.objects.filter(
            status=Mailing.STARTED,
            start_sending__lte=current_time,
            end_sending__gte=current_time
        ).prefetch_related('recipients', 'letter')

        mailing_count = active_mailings.count()
        self.stdout.write(f'Найдено активных рассылок: {mailing_count}')

        # Обработка каждой рассылки
        for mailing in active_mailings:
            self.stdout.write(f'\nОбработка рассылки #{mailing.id} ({mailing})')

            # Получение данных письма
            subject = mailing.letter.title if mailing.letter else 'Без темы'
            message = mailing.letter.description if mailing.letter else ''

            # Получение списка получателей
            recipients = mailing.recipients.all()
            total_recipients = recipients.count()

            if not total_recipients:
                self.stdout.write(self.style.WARNING('  X Нет получателей для рассылки'))
                continue

            self.stdout.write(f'  Получателей: {total_recipients}')

            # Отправка писем каждому получателю
            success_count = 0
            for recipient in recipients:
                attempt = AttemptToSend(mailing=mailing)
                recipient_email = recipient.email

                try:
                    # Отправка письма конкретному получателю
                    send_mail(
                        subject=subject,
                        message=message,
                        from_email=EMAIL_HOST_USER,
                        recipient_list=[recipient_email],
                        fail_silently=False
                    )

                    # Фиксация успешной попытки
                    attempt.status = AttemptToSend.SUCCESS
                    attempt.mail_server_response = 'Успешно доставлено'
                    attempt.save()
                    success_count += 1
                    self.stdout.write(f'  V [Успех] {recipient_email}')

                except Exception as e:
                    # Фиксация неудачной попытки
                    error_msg = str(e)
                    attempt.status = AttemptToSend.FAILED
                    attempt.mail_server_response = f'Ошибка: {error_msg}'
                    attempt.save()
                    self.stdout.write(self.style.ERROR(f'  X [Ошибка] {recipient_email}: {error_msg}'))

            # Статистика по рассылке
            success_rate = (success_count / total_recipients) * 100 if total_recipients else 0
            self.stdout.write(
                self.style.SUCCESS(f'  ИТОГ: Отправлено {success_count}/{total_recipients} '
                f'({success_rate:.1f}%)') if success_count == total_recipients
                else self.style.WARNING(f'  ИТОГ: Отправлено {success_count}/{total_recipients}'
                f'({success_rate:.1f}%)')
            )

        self.stdout.write(self.style.SUCCESS('\nОбработка рассылок завершена!'))
