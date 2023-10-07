from datetime import datetime, timedelta
from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail

from users.models import User
from course.models import Subscription, Course


@shared_task
def send_mail_user_course_update(course_id):
    """
    Функция отправляет асинхронную рассылку писем пользователям об обновлении материалов курса.
    """

    subscribers_list = Subscription.objects.filter(course_id=course_id, status=True)
    course = Course.objects.get(id=course_id)

    for sub in subscribers_list:
        print(f"Отправка сообщения по подписке {sub}")
        send_mail(
            subject=f'Обновление курса {course.name}',
            message=f'Уведомляем Вас о том, что появились новые материалы для Вашего курса',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[sub.user.email]
        )


@shared_task
def check_deactivate_user():
    """
    Функция проверяет активность пользователей и деактивирует неактивных в течении 30 дней.
    """
    now_time = datetime.now()
    one_month_ago = now_time - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago)
    inactive_users.update(is_active=False)
    print(f'Выявлены следующие неактивные пользователи {inactive_users}')

    # Отправляем сообщение неактивному пользователю
    if inactive_users is not None:
        send_mail(
            subject=f'Деактивация',
            message=f'Вы не были активны в течении 30 дней, поэтому мы Вас, к сожалению, деактивировали',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[inactive_users.email]
        )
