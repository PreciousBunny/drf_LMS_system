import pytest
from django.urls import reverse
from rest_framework import status

from tests.conftest import *
from course.models import Lesson
from course.serializers import LessonSerializer


# # Проверка правильной установки и настройки pytest-django
# def test_l():
#     assert True


@pytest.mark.django_db
class TestLessonViews:

    def test_list_lessons(self, client, user, lesson):
        url = reverse('course:lesson_list')
        client.force_authenticate(user=user)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_create_lesson(self, client, superuser, course):
        url = reverse('course:lesson_create')
        client.force_authenticate(user=superuser)
        data = {
            'name': 'New Lesson',
            'description': 'New Lesson Description',
            'course': course.id,
            'url_video': 'https://www.youtube.com/testlesson'
        }
        response = client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Lesson.objects.filter(name='New Lesson').exists()

    def test_retrieve_lesson(self, client, user, lesson):
        url = reverse('course:lesson_detail', kwargs={'pk': lesson.id})
        client.force_authenticate(user=user)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert LessonSerializer(lesson).data == response.data

    def test_update_lesson(self, client, user, lesson):
        url = reverse('course:lesson_update', kwargs={'pk': lesson.id})
        client.force_authenticate(user=user)
        data = {'name': 'Updated Lesson'}
        response = client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert Lesson.objects.get(id=lesson.id).name == 'Updated Lesson'

    def test_delete_lesson(self, client, superuser, lesson):
        url = reverse('course:lesson_delete', kwargs={'pk': lesson.id})
        client.force_authenticate(user=superuser)
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Lesson.objects.filter(id=lesson.id).exists()
