from django.core.management.base import BaseCommand
from users.models import User
from course.models import Course, Lesson, Payment
from faker import Faker
import random


fake = Faker()


# attention! execute the program with the command: >_ python manage.py create_data

class Command(BaseCommand):
    """
    Команда для сброса и добавления тестовых данных в модель Payment.

    Метод `handle` выполняет следующие шаги:
    1. Удаляет все записи в моделях User, Payment, Lesson и Course.
    2. Создает 5 пользователей и сохраняет их в список.
    3. Создает 5 курсов и для каждого курса создает 3 урока.
    4. Создает 20 случайных платежей, связанных с пользователями, курсами и уроками.
    """

    def handle(self, *args, **kwargs):
        print("Привет! Начинаю заполнять БД - Wait few minutes!")

        User.objects.all().delete()
        Payment.objects.all().delete()
        Lesson.objects.all().delete()
        Course.objects.all().delete()

        users = []
        for _ in range(5):
            email = fake.email()
            password = fake.password()
            phone = fake.numerify('+1(###)#######')
            city = fake.city()
            user = User.objects.create(email=email, password=password, phone=phone, city=city)
            users.append(user)

        courses = []
        lessons = []
        for _ in range(5):
            course = Course.objects.create(
                name=fake.word(),
                description=fake.text(),
            )
            courses.append(course)

            for _ in range(3):
                lesson = Lesson.objects.create(
                    name=fake.sentence(),
                    description=fake.text(),
                    course=course,
                    url_video=fake.url(),
                )
                lessons.append(lesson)

        for _ in range(20):
            user = random.choice(users)
            payment_date = fake.date_between(start_date='-30d', end_date='today')
            payment_sum = fake.pyint(min_value=10000, max_value=300000)
            payment_type = random.choice(['cash', 'transfer'])

            is_course = random.choice([True, False])
            course_or_lesson = random.choice(courses) if is_course else random.choice(lessons)

            Payment.objects.create(
                user=user,
                payment_date=payment_date,
                course=course_or_lesson if is_course else None,
                lesson=course_or_lesson if not is_course else None,
                payment_sum=payment_sum,
                payment_type=payment_type,
            )
