from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from materials.models import Course, Lesson, Subscription
from materials.paginators import LessonPaginator
from materials.serializer import CourseSerializer, LessonSerializer, SubscriptionSerializer
from users.permissions import IsModer, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """ Отвечает за курсы """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = LessonPaginator

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (~IsModer, IsAuthenticated)

        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (IsAuthenticated, IsModer | IsOwner,)

        elif self.action == 'destroy':
            self.permission_classes = (IsAuthenticated, ~IsModer | IsOwner,)

        elif self.action in "list":
            self.permission_classes = (IsAuthenticated,)

        return [permission() for permission in self.permission_classes]


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

    def post(self):
        user = self.request.user
        course_id = self.request.data.get('course_id')
        course_item = Course.objects.get_object_or_404(Course, pk=course_id)

        subs_item = Subscription.objects.filter(
            user=user, course_subscription=course_item
        )

        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            Subscription.objects.create(user=user, course_subscription=course_item)
            message = 'подписка добавлена'
        # Возвращаем ответ в API
        return Response({"message": message})
