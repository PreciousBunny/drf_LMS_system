import requests
from django.conf import settings

from course.models import Payment

api_key = settings.STRIPE_SECRET_KEY
headers = {'Authorization': f'Bearer {api_key}'}
base_url = 'https://api.stripe.com/v1'


def create_payment(course, user):
    """
    Функция запрашивает данные с сервиса об осуществлении платежа с сервиса Stripe.
    """
    data = [
        ('amount', course.price),
        ('currency', 'usd'),
    ]
    # Запрашиваем данные с сервиса
    response = requests.post(f'{base_url}/payment_intents', headers=headers, data=data)
    if response.status_code != 200:
        raise Exception(f'ошибка осуществления платежа: {response.json()["error"]["message"]}')
    return response.json()


def save_payment(course, user):
    """
    Функция заносит данные о платеже в базу данных с сервиса Stripe.
    """
    Payment.objects.create(
        user=user,
        course=course,
        payment_sum=course.price,
    )
