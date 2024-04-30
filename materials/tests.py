from rest_framework.test import APITestCase, APIClient
from users.models import User
from materials.models import Lesson, Course, Subscription
from django.urls import reverse
from rest_framework import status


class LessonTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(email='test@test.com', password='12345')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(name='test', owner=self.user)
        self.lesson = Lesson.objects.create(name='test', course=self.course,
                                            url='https://www.youtube.com/123',
                                            owner=self.user)

    def test_list_lessons(self):
        response = self.client.get(
            reverse('materials:lesson_list'),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'count': 1, 'next': None, 'previous': None,
             'results': [{'id': 4, 'course': self.course.pk, 'name': self.course.name,
                          'description': None, 'preview': None, 'video': None,
                          'owner': self.user.pk, 'url': 'https://www.youtube.com/123'}]}
        )

    def test_create_lesson(self):
        data = {
            "name": self.lesson.name,
            "course": self.course.id,
            "url": "https://www.youtube.com/123",
        }
        response = self.client.post(reverse('materials:lesson_create'), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.json(),
                         {'id': 2, 'course': self.course.pk, 'name': self.course.name,
                          'description': None, 'preview': None, 'video': None,
                          'owner': self.user.pk, 'url': 'https://www.youtube.com/123'})

    def test_retrieve_lesson(self):
        response = self.client.get(
            reverse('materials:lesson_retrieve', kwargs={'pk': self.lesson.pk}),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(response.json(),
                         {'id': 5, 'course': self.course.pk, 'name': self.course.name,
                          'description': None, 'preview': None, "video": None,
                          'owner': self.user.pk, 'url': 'https://www.youtube.com/123'})

    def test_update_lesson(self):
        data = {
            "name": "test",
            "course": self.course,
            "url": "https://www.youtube.com/123",
            "owner": self.user,
        }
        response = self.client.patch(
            reverse('materials:lesson_update', kwargs={'pk': self.lesson.pk}),


            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': 6, 'course': 1, 'name': 'test',
             'url': 'https://www.youtube.com/123', 'owner': self.user}
        )

    def test_delete_lesson(self):
        response = self.client.delete(
            reverse('materials:lesson_delete', kwargs={'pk': self.lesson.pk}),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_validator(self):
        data = {
            "name": "test",
            "course": "test",
            "video": "https://www.test.com/54321"
        }
        response = self.client.post(reverse('materials:lesson_create'), data=data)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # self.assertEqual(
        #     response.json(),
        #     {'non_field_errors': ['Incorrect YouTube URL']}
        # )


class SubscriptionTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(email='test@test.com', password='12345')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(name="test", owner=self.user)
        self.subscription = Subscription.objects.create(course_subscription=self.course, user=self.user)

    def test_create_subscription(self):
        data = {
            "user": self.user.id,
            "course_subscription": self.course.id,
        }

        response = self.client.post(reverse('materials:subscription-create'), data=data)

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        (self.assertEquals(
            response.json(),
            'подписка удалена'
        ))
