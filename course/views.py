from rest_framework import generics, viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from course.models import Course, Lesson, Payment
from course.paginations import CoursePagination, LessonPagination
from course.permissions import UserPermissionsModerator, UserPermissionsOwner
from course.serializers import CourseSerializer, LessonSerializer, PaymentSerializer
from users.models import UserRoles


# Create your views here.


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursePagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Метод выводи список всех курсов модераторам или администратору, владельцам - только созданные им курсы.
        """
        user = self.request.user
        if user.is_staff or user.role == UserRoles.MODERATOR or user.is_superuser:
            return Course.objects.all()
        else:
            return Course.objects.filter(owner=user)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = LessonPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Метод выводи список всех уроков модераторам или администратору, владельцам - только созданные им уроки.
        """
        user = self.request.user
        if user.is_staff or user.role == UserRoles.MODERATOR or user.is_superuser:
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [UserPermissionsModerator | UserPermissionsOwner]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [UserPermissionsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [UserPermissionsModerator | UserPermissionsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [UserPermissionsOwner]


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['payment_type', 'course', 'lesson']
    search_fields = ['payment_type', 'course', 'lesson']
    ordering_fields = ['payment_date']
    permission_classes = [IsAuthenticated]


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]

