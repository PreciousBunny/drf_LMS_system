import pytest
from rest_framework.test import APIClient

from course.models import Course, Lesson, Subscription
from users.models import User


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create(email='testuser@example.com',
                               password='testpassword', role='moderator')


@pytest.fixture
def superuser():
    superuser = User.objects.create(
        email='testadmin@example.com',
        password='testpassword',
        first_name='Admin',
        last_name='Adm',
        is_staff=True,
        is_superuser=True
    )
    return superuser


@pytest.fixture
def course():
    return Course.objects.create(name='Test Course', description='Test Course Description')


@pytest.fixture
def lesson(course):
    return Lesson.objects.create(name='Test Lesson', description='Test Lesson Description', course=course)


@pytest.fixture
def subscription(user, course):
    return Subscription.objects.create(user=user, course=course)
