from django.core.mail import send_mail
from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from materials.models import Course, Lesson, Subscription
from materials.paginators import LessonPaginator
from materials.serializer import CourseSerializer, LessonSerializer, SubscriptionSerializer
from materials.tasks import my_send_email
from users.models import User
from users.permissions import IsModer, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """ Отвечает за курсы """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = LessonPaginator

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (~IsModer, IsAuthenticated)

        elif self.action in 'update':
            self.permission_classes = (IsAuthenticated, IsModer | IsOwner,)

        elif self.action == 'destroy':
            self.permission_classes = (IsAuthenticated, ~IsModer | IsOwner,)

        elif self.action in ("list", 'retrieve', "subscribe"):
            self.permission_classes = (IsAuthenticated,)

        return [permission() for permission in self.permission_classes]

    @action(detail=True, methods=['GET'])
    def subscribe(self, request, pk=None, ):
        """Метод для подписки на курс"""
        user = request.user
        course_item = Course.objects.filter(id=pk).first() or Course.objects.get(Course, pk=pk)

        if Subscription.objects.filter(user=user, course_subscription=course_item).exists():
            Subscription.objects.filter(user=user, course_subscription=course_item).delete()
            message = 'подписка отменена'
            return Response({"message": message})
        else:
            Subscription.objects.create(user=user, course_subscription=course_item)
            message = 'подписка оформлена'
            return Response({"message": message})

    def update(self, request, *args, **kwargs):
        """ Отправка пользователям имеющим подписку на курс информации об обновлении курса """
        # Список пользователей подписанных на курс
        recipient_list = Subscription.objects.filter(Course, course_subscription=True)

        my_send_email.delay(recipient_list)

        return super().update(request, *args, **kwargs)


class LessonListAPIView(generics.ListAPIView):
    """ Отвечает за просмотр списка Уроков"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = LessonPaginator


class LessonCreateAPIView(generics.CreateAPIView):
    """ Отвечает за создание сущности Урок"""
    serializer_class = LessonSerializer
    permission_classes = (~IsModer, IsAuthenticated)

    def perform_create(self, serializer):
        my_send_email.delay()
        serializer.save(owner=self.request.user)


class LessonUpdateAPIView(generics.UpdateAPIView):
    """ Отвечает за редактирование сущности Урок"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModer | IsOwner,)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """ Отвечает за просмотр сущности Урок"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModer | IsOwner,)


class LessonDestroyAPIView(generics.DestroyAPIView):
    """ Отвечает за удаление сущности Урок"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsOwner | ~IsModer)


class CoursesSubscriptionViewSet(viewsets.ModelViewSet):
    """
    Логика подписки
    """
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    queryset = Subscription.objects.all()

