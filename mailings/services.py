from django.core.cache import cache
from config.settings import CACHE_ENABLED
from .models import Recipients, Letter, Mailing, AttemptToSend


def get_cached_recipients(user):
    """Кеширование списка клиентов"""
    key = f'recipients_{"managers" if user.groups.filter(name="managers").exists() else user.id}'

    if not CACHE_ENABLED:
        return Recipients.objects.all() if user.groups.filter(name='managers').exists() else Recipients.objects.filter(owner=user)

    recipients = cache.get(key)
    if recipients is None:
        recipients = list(Recipients.objects.all() if user.groups.filter(name='managers').exists() else Recipients.objects.filter(owner=user))
        cache.set(key, recipients, timeout=60*5) # 5 минут
    return recipients


def get_cached_letters(user):
    """Кеширование списка писем"""
    key = f'letters_{"manager" if user.groups.filter(name="managers").exists() else user.id}'

    if not CACHE_ENABLED:
        return Letter.objects.all() if user.groups.filter(name='managers').exists() else Letter.objects.filter(
            owner=user)

    letters = cache.get(key)
    if letters is None:
        letters = list(
            Letter.objects.all() if user.groups.filter(name='managers').exists() else Letter.objects.filter(owner=user))
        cache.set(key, letters, timeout=60 * 5)
    return letters


def get_cached_mailings(user):
    """Кеширование списка рассылок"""
    key = f'mailings_{"all" if user.is_superuser or user.has_perm("users.can_disable_user") else user.id}'

    if not CACHE_ENABLED:
        if user.is_superuser or user.has_perm('users.can_disable_user'):
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=user)

    mailings = cache.get(key)
    if mailings is None:
        mailings = list(Mailing.objects.all() if user.is_superuser or user.has_perm(
            'users.can_disable_user') else Mailing.objects.filter(owner=user))
        cache.set(key, mailings, timeout=60 * 5)
    return mailings


def get_cached_attempts(user):
    """Кеширование списка попыток отправки"""
    key = f'attempts_{"all" if user.is_superuser or user.has_perm("users.can_disable_user") else user.id}'

    if not CACHE_ENABLED:
        if user.is_superuser or user.has_perm('users.can_disable_user'):
            return AttemptToSend.objects.all()
        return AttemptToSend.objects.filter(owner=user)

    attempts = cache.get(key)
    if attempts is None:
        attempts = list(AttemptToSend.objects.all() if user.is_superuser or user.has_perm(
            'users.can_disable_user') else AttemptToSend.objects.filter(owner=user))
        cache.set(key, attempts, timeout=60 * 5)
    return attempts
