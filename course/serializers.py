from rest_framework import serializers

from course.models import *


class LessonSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    lessons_count = serializers.SerializerMethodField()  # поле вывода количества уроков в курсе
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True, )  # поле вывода уроков курса

    def get_lessons_count(self, instance):
        # метод определяет количество уроков в курсе
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
