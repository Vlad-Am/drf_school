from django.urls import path
from rest_framework.routers import DefaultRouter

from materials.apps import MaterialsConfig
from materials.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonUpdateAPIView, \
    LessonDestroyAPIView, LessonRetrieveAPIView, CoursesSubscriptionViewSet

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')  # Курс
router.register(r'subscription', CoursesSubscriptionViewSet, basename='subscription')  # Подписка

urlpatterns = [
                  path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),  # Создание урока
                  path('lesson/', LessonListAPIView.as_view(), name='lesson_list'),  # Список уроков
                  path('lesson/<int:pk>/update', LessonUpdateAPIView.as_view(), name='lesson_update'),  # Редактирование
                  path('lesson/<int:pk>/delete', LessonDestroyAPIView.as_view(), name='lesson_delete'),  # Удаление
                  path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_retrieve'),  # Просмотр

              ] + router.urls
