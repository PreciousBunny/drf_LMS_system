from django.urls import path
from rest_framework.routers import DefaultRouter

from course.views import *
from course.apps import CourseConfig

app_name = CourseConfig.name


router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')


urlpatterns =[
    # Lesson
    path('lesson', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/detail/<int:pk>', LessonRetrieveAPIView.as_view(), name='lesson_detail'),
    path('lesson/create', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/update/<int:pk>', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>', LessonDestroyAPIView.as_view(), name='lesson_delete'),

    # Payment
    path('payment', PaymentListAPIView.as_view(), name='payment_list'),
    path('payment/create', PaymentCreateAPIView.as_view(), name='payment_create'),
    path('payment/detail/<int:pk>', PaymentRetrieveAPIView.as_view(), name='payment_detail'),

    # Subscription
    path('subscribe/<int:course_id>', SubscribeCourseView.as_view(), name='subscribe_course'),
    path('unsubscribe/<int:course_id>', UnsubscribeCourseView.as_view(), name='unsubscribe_course'),
    ] + router.urls
