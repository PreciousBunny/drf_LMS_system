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
    price = models.PositiveIntegerField(default=10000, verbose_name='Стоимость курса')

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


class Payment(models.Model):
    """
    Класс описания модели Платежей (Оплаты).
    """
    # Установим флаги со способом оплаты
    CASH = 'cash'
    TRANSFER = 'transfer'

    PAYMENT_TYPE = [
        (CASH, 'cash'),
        (TRANSFER, 'transfer')
    ]

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Пользователь')
    payment_date = models.DateField(auto_now_add=True, verbose_name='Дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Оплаченный курс', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Оплаченный урок', **NULLABLE)
    payment_sum = models.PositiveIntegerField(verbose_name='сумма оплаты')
    payment_type = models.CharField(choices=PAYMENT_TYPE, max_length=30, default=TRANSFER, verbose_name='способ оплаты')

    def __str__(self):
        return f'Payment({self.user}, {self.course if self.course else self.lesson} - {self.payment_sum}, {self.payment_date})'

    class Meta:
        """
        Класс мета-настроек.
        """
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'


class Subscription(models.Model):
    """
    Класс описания модели Подписки на курс.

    """
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name="Пользователь")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")
    is_active = models.BooleanField(default=False, verbose_name='Статус подписки')

    def __str__(self):
        return f'{self.user} подписан на {self.course.name}'

    class Meta:
        """
        Класс мета-настроек.
        """
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
