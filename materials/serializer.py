from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import validate_youtube_url


class SubscriptionSerializer(serializers.ModelSerializer):
    """ Сериализатор модели подписки"""

    class Meta:
        model = Subscription
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    url = serializers.URLField(validators=[validate_youtube_url])

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = serializers.SerializerMethodField()
    subject_list = LessonSerializer(source='lesson_set', many=True, read_only=True)
    is_sub = serializers.SerializerMethodField(read_only=True)  # поле подписки на курс

    def get_is_sub(self, course):
        owner = self.context['request'].user
        subscription = Subscription.objects.filter(course_subscription=course.id, user=owner.id)
        if subscription:
            return True
        return False

    @staticmethod
    def get_count_lessons(instance):
        if instance.lessons:
            return instance.lessons.count()
        else:
            return 0

    class Meta:
        model = Course
        fields = ('id', 'name', 'description',  'count_lessons', 'subject_list', 'owner',
                  'is_sub')
