from rest_framework import serializers


def url_validator(url_video):
    """
    Функция проверяет, является ли URL допустимым для использования или нет.
    """
    if not url_video.startswith('https://www.youtube.com/'):
        raise serializers.ValidationError('Использование стороннего ресурса! Ссылка возможна только с youtube.com!')
