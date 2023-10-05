from django.contrib import admin
from course.models import *


# Register your models here.


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'preview', 'description', 'owner',)
    list_filter = ('name',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'preview', 'description', 'owner', 'url_video',)
    list_filter = ('name',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_date', 'course', 'lesson', 'payment_sum', 'payment_type')
    list_filter = ('user', 'payment_date', 'payment_type',)
