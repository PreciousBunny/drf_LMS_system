from django.db import models
from users.models import User

# Create your models here.


NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    """
    Класс описания модели Курса.
    """
    name = models.CharField(max_length=255, verbose_name='Название курса')
    preview = models.ImageField(upload_to='course/', verbose_name='Изображение', **NULLABLE)
    description = models.TextField(verbose_name='Описание курса', **NULLABLE)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Создатель', **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        """
        Класс мета-настроек.
        """
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    """
    Класс описания модели Урока.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    name = models.CharField(max_length=255, verbose_name='Название урока')
    description = models.TextField(verbose_name='Описание урока', **NULLABLE)
    preview = models.ImageField(upload_to='lesson/', verbose_name='Изображение', **NULLABLE)
    url_video = models.URLField(verbose_name='Ссылка на видео', **NULLABLE)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Создатель', **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        """
        Класс мета-настроек.
        """
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
