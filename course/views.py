from rest_framework import generics, viewsets, status
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from course.models import Course, Lesson, Payment, Subscription
from course.paginations import CoursePagination, LessonPagination
from course.permissions import UserPermissionsModerator, UserPermissionsOwner
from course.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer
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


class SubscribeCourseView(generics.CreateAPIView):
    """
    Класс создает подписку пользователя на выбранный курс.
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        course_id = kwargs.get('course_id')
        course = Course.objects.get(pk=course_id)

        # Проверка подписки пользователя на определенный курс
        if Subscription.objects.filter(user=request.user, course=course).exists():
            return Response({'detail': 'Вы уже подписаны на этот курс!'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data={'user': request.user.id, 'course': course.id})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        active_subscription = Subscription.objects.filter(user=request.user, course=course)
        active_subscription.update(is_active=True)

        return Response({'detail': 'Вы успешно подписались на курс! Успехов Вам!'}, status=status.HTTP_201_CREATED)


class UnsubscribeCourseView(generics.DestroyAPIView):
    """
    Класс удаляет подписку пользователя по выбранному курсу.
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        course_id = self.kwargs.get('course_id')
        course = Course.objects.get(pk=course_id)
        return Subscription.objects.get(user=self.request.user, course=course)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'detail': 'Вы успешно отписались от курса! Ждем Вас снова!'}, status=status.HTTP_200_OK)
