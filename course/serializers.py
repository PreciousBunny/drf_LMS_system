from rest_framework import serializers

from course.models import *
from course.validators import url_validator


class LessonSerializer(serializers.ModelSerializer):
    # Сокрытие поля "Создатель" и автоматическая привязка его к пользователю
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    # проверка допустимого url_video
    url_video = serializers.URLField(validators=[url_validator])

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    # Сокрытие поля "Создатель" и автоматическая привязка его к пользователю
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    # поле вывода количества уроков в курсе
    lessons_count = serializers.SerializerMethodField()
    # поле вывода уроков курса
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True, )

    def get_lessons_count(self, instance):
        """
        Метод определяет количество уроков в курсе.
        """
        lessons = Lesson.objects.filter(course=instance).all()
        if lessons:
            return lessons.count()
        return 0

    class Meta:
        model = Course
        fields = ('id', 'owner', 'name', 'preview', 'description', 'lessons', 'lessons_count',)


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
